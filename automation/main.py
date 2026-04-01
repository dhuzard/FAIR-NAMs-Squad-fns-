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
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()
console = Console()

AGENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "agents")
DB_DIR = os.path.join(os.path.dirname(__file__), "db")

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

@app.command()
def ingest():
    """
    Ingest all agent Knowledge Bases into the Vector DB.
    """
    from ingest import main as ingest_main
    ingest_main()

if __name__ == "__main__":
    app()
