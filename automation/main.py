import os
import typer
from rich.console import Console
from rich.markdown import Markdown
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Sequence, Literal
import operator
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()
console = Console()

AGENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "agents")
DB_DIR = os.path.join(os.path.dirname(__file__), "db")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

class RouteDecision(BaseModel):
    next: Literal["BioEthos", "Semantica", "TechLead", "FINISH"] = Field(
        ..., description="The next agent to route to, or FINISH if the task is complete."
    )

def get_agent_persona(agent_name: str) -> str:
    persona_path = os.path.join(AGENTS_DIR, agent_name, "persona.md")
    if os.path.exists(persona_path):
        with open(persona_path, "r", encoding="utf-8") as f:
            return f.read()
    return "You are a helpful assistant."

def get_retriever(agent_name: str):
    persist_directory = os.path.join(DB_DIR, agent_name)
    if not os.path.exists(persist_directory):
        return None
    
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
    return vectorstore.as_retriever()

@app.command()
def chat(agent_name: str):
    """
    Chat with a specific agent (BioEthos, Semantica, TechLead, DrNexus).
    """
    if not os.path.isdir(os.path.join(AGENTS_DIR, agent_name)):
        console.print(f"[red]Agent '{agent_name}' not found.[/red]")
        return

    console.print(f"[bold green]Starting chat with {agent_name}...[/bold green]")
    system_prompt_text = get_agent_persona(agent_name)
    retriever = get_retriever(agent_name)

    # Initialize LLM (Ensure OPENAI_API_KEY is set in .env)
    try:
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    except Exception as e:
        console.print("[red]Error initializing LLM. Check your OPENAI_API_KEY.[/red]")
        return

    # Define RAG Chain
    template = """
    Answer the question based only on the following context:
    {context}

    ---
    System Persona:
    {persona}
    ---
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    if retriever:
        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough(), "persona": lambda x: system_prompt_text}
            | prompt
            | llm
            | StrOutputParser()
        )
    else:
        console.print("[yellow]No Knowledge Base found. Chatting with raw persona.[/yellow]")
        # Fallback chain without RAG
        fallback_template = """
        System Persona:
        {persona}
        ---
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(fallback_template)
        chain = (
            {"question": RunnablePassthrough(), "persona": lambda x: system_prompt_text}
            | prompt
            | llm
            | StrOutputParser()
        )

    while True:
        question = typer.prompt("You")
        if question.lower() in ["exit", "quit"]:
            break
        
        response = chain.invoke(question)
        console.print(Markdown(f"**{agent_name}**: {response}"))

def make_agent_node(agent_name: str, llm):
    persona = get_agent_persona(agent_name)
    retriever = get_retriever(agent_name)
    
    def node(state: AgentState):
        messages = state["messages"]
        last_msg = messages[-1].content
        
        context_str = ""
        if retriever:
            docs = retriever.invoke(last_msg)
            context_str = "\n\n".join([d.page_content for d in docs])
            
        system_prompt = f"System Persona:\n{persona}\n\nContext:\n{context_str}"
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        chain = prompt | llm
        response = chain.invoke({"messages": messages})
        return {"messages": [AIMessage(content=response.content, name=agent_name)]}
        
    return node

def supervisor_node(state: AgentState, llm):
    system_prompt = (
        "You are Dr. Nexus, the Orchestrator.\n"
        "Your job is to manage a swarm of agents: BioEthos (Ethics/3Rs), Semantica (Ontologies/FAIR), and TechLead (Code/Architecture).\n"
        "Read the conversation history. Decide who should speak next to fulfill the user's overarching request.\n"
        "If you have enough information from the agents to fully satisfy the user's initial request, respond with FINISH."
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Given the conversation above, who should act next? Or should we FINISH?")
    ])
    
    supervisor_chain = prompt | llm.with_structured_output(RouteDecision)
    decision = supervisor_chain.invoke({"messages": state["messages"]})
    return {"next": decision.next}

@app.command()
def swarm(question: str):
    """
    Launch the Multi-Agent Swarm (Dr. Nexus, BioEthos, Semantica, TechLead).
    """
    try:
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    except Exception as e:
        console.print("[red]Error initializing LLM. Check your OPENAI_API_KEY.[/red]")
        return
        
    workflow = StateGraph(AgentState)
    
    workflow.add_node("BioEthos", make_agent_node("BioEthos", llm))
    workflow.add_node("Semantica", make_agent_node("Semantica", llm))
    workflow.add_node("TechLead", make_agent_node("TechLead", llm))
    workflow.add_node("DrNexus", lambda state: supervisor_node(state, llm))
    
    for member in ["BioEthos", "Semantica", "TechLead"]:
        workflow.add_edge(member, "DrNexus")
        
    conditional_map = {k: k for k in ["BioEthos", "Semantica", "TechLead"]}
    conditional_map["FINISH"] = END
    
    workflow.add_conditional_edges("DrNexus", lambda x: x["next"], conditional_map)
    workflow.add_edge(START, "DrNexus")
    
    graph = workflow.compile()
    
    console.print(f"[bold green]Starting Swarm orchestration...[/bold green]")
    console.print(Markdown(f"**Objective**: {question}"))
    
    for s in graph.stream({"messages": [HumanMessage(content=question)]}, {"recursion_limit": 15}):
        if "__end__" not in s:
            for node_name, output in s.items():
                if "messages" in output:
                    msg = output["messages"][-1]
                    console.print(Markdown(f"**{node_name}**: {msg.content}"))
                elif "next" in output:
                     if output["next"] != "FINISH":
                         console.print(f"\n[bold yellow]➡️  Dr. Nexus delegates to {output['next']}...[/bold yellow]")
                     else:
                         console.print(f"\n[bold green]✅ Dr. Nexus concludes the task.[/bold green]")

@app.command()
def ingest():
    """
    Ingest all agent Knowledge Bases into the Vector DB.
    """
    from ingest import main as ingest_main
    ingest_main()

if __name__ == "__main__":
    app()
