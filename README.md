# FAIR-NAMs-Squad 🐁🦉⚙️

**Horizon Europe Active Research Swarm**

This repository hosts a Multi-Agent System (MAS) designed to validate "Metadatapp" as a tool for Virtual Control Groups (VCGs) and New Approach Methodologies (NAMs). The squad consists of specialized AI agents, each with a distinct Knowledge Base (KB) and persona.

---

## 🚀 The Squad

| Agent | Icon | Role | Focus Areas |
| :--- | :---: | :--- | :--- |
| **Dr. Nexus** | 👑 | **Orchestrator** | Synthesis, Gap Analysis, Conflict Resolution. |
| **BioEthos** | 🐁 | **Ethics Officer** | 3Rs (Reduction, Replacement, Refinement), EU Directive 2010/63/EU, Statistical Validity. |
| **Semantica** | 🦉 | **Ontologist** | FAIR Principles, W3C Standards, Ontologies (SSN, EFO, PROV-O). |
| **TechLead** | ⚙️ | **Architect** | Symfony, API Platform, Hydra, JSON-LD, System Design. |

---

## 🧠 How to Interact (Prompting Guide)

To get the best results from this squad, use the **"Role-Based Invocation"** pattern in your prompts.

### 1. The "Council of Elrond" Pattern
Use this when you have a complex problem requiring diverse perspectives.
> **Prompt:** "Dr. Nexus, convene the swarm. Topic: [Your Topic]. Ask BioEthos about the ethical implications, Semantica about the data modeling, and TechLead about the implementation."

### 2. The "Direct Interrogation" Pattern
Use this when you need deep expertise in one domain.
> **Prompt:** "@Semantica, I have a CSV file with columns 'Date', 'CageID', 'Activity'. Map this to the SSN ontology and generating a SHACL validation shape."

### 3. The "Knowledge Injection" Pattern
Use this to teach the agents new facts.
> **Prompt:** "I have added `new_regulation.pdf` to BioEthos's KB. BioEthos, please read it and summarize how it affects our VCG strategy."

---

## 📂 Repository Structure

```
rubric
├── agents/
│   ├── BioEthos/       # Ethics Agent
│   │   ├── KB/         # Drop PDFs/Text here for BioEthos to read
│   │   └── persona.md  # System Prompt / Character Sheet
│   ├── Semantica/      # Ontology Agent
│   │   ├── KB/         # Drop Ontologies/RDF here
│   │   └── persona.md
│   ├── TechLead/       # Architecture Agent
│   │   ├── KB/         # Drop Code/Configs here
│   │   └── persona.md
│   └── DrNexus/        # Orchestrator
│       ├── KB/
│       └── persona.md
└── README.md
```

---

## 🔍 Critical Review & Roadmap

### Current Limitations
1.  **Manual Context Loading**: Currently, the AI (Me) must manually "read" the files in the `KB` folders. There is no automated vector database or RAG pipeline.
2.  **No Execution Environment**: The agents are "simulated" personas. They cannot autonomously run PHP code or executing SPARQL queries unless I (the AI) run the tools for them.
3.  **Static Personas**: The `persona.md` files are static. They do not evolve automatically based on conversation history unless manually updated.

### Critical Improvements (Roadmap)
-   [ ] **Automated RAG Pipeline**: Implement a script (Python/LangChain) that watches the `KB` folders, chunks documents, and embeds them into a local vector store (e.g., ChromaDB).
-   [ ] **Agentic CLI**: Create a simple CLI tool (`./squad chat`) that allows you to chat with a specific agent directly in the terminal, loading their specific context.
-   [ ] **CI/CD Integration**: TechLead should be able to trigger GitHub Actions to run tests or validate ontology files (SHACL) automatically.
-   [ ] **Memory Persistence**: Implement a `memory.json` for each agent to store "learned" facts across different sessions.

---

## 🛠️ Setup & Usage

1.  **Enrich the Squad**: Place relevant documents in `agents/{Agent}/KB`.
2.  **Start a Session**: Open a chat and say: *"Initialize the FAIR-NAMs-Squad context."*
3.  **Collaborate**: Use the prompting patterns above to drive the research.
