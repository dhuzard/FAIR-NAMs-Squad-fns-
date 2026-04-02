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

## 🚀 Version 2.0 Architectural Upgrades
The squad has been upgraded from a static RAG pipeline to an event-driven **LangGraph Multi-Agent State Machine**. 

### Active Capabilities
-   **Live Web Browsing:** Dr. Nexus and Semantica can actively search the live web using the **You.com API** and the **PubMed API**, breaking free from static local PDFs.
-   **Autonomous File I/O:** The Scribe agent can progressively write manuscript sections directly to the local disk (`Drafts/` directory).
-   **Semantic Validation:** Agents can perform live lookups against `Schema.org`.

## 🔍 Future Roadmap
While Phase 1 (Data Schema mapping) and Phase 2 (LangGraph Tools) are complete, further technical evolution is required to hit production readiness.

👉 **View the full development pipeline in our roadmap:** [`Future_Improvements_TODO.md`](Future_Improvements_TODO.md)

---

## 🛠️ Setup & Usage

1.  **Enrich the Squad**: Place relevant documents in `agents/{Agent}/KB`.
2.  **Start a Session**: Open a chat and say: *"Initialize the FAIR-NAMs-Squad context."*
3.  **Collaborate**: Use the prompting patterns above to drive the research.
