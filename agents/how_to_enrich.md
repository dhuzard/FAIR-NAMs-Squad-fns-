# How to Enrich the Swarm 🧠

This repository is set up for a "Multi-Agent Swarm" simulation. You can "teach" the agents by adding documents to their Knowledge Base (KB) folders.

## Directory Structure
```
agents/
  ├── BioEthos/   (Ethics, 3Rs, Stats)
  │   └── KB/     <-- Drop PDFs, MDs, or Text files here
  ├── Semantica/  (Ontologies, FAIR)
  │   └── KB/     <-- Drop RDF, TTL, or Ontology docs here
  ├── TechLead/    (Symfony, Architecture)
  │   └── KB/     <-- Drop Code snippets, Configs, or Docs here
  └── DrNexus/     (Orchestrator)
      └── KB/     <-- Drop Project Requirements or Goals here
```

## How to Use
1.  **Identify the Topic**:
    -   Is it about *Animal Welfare*? -> **BioEthos**.
    -   Is it about *Data Standards*? -> **Semantica**.
    -   Is it about *Code/Infrastructure*? -> **TechLead**.
2.  **Add the File**:
    -   Copy the file (PDF, Markdown, Text) into the corresponding `KB/` folder.
3.  **Notify the Swarm**:
    -   In your chat with the AI, mention: "I have added [Filename] to BioEthos's KB. Please digest it."

## Agent Capabilities
The agents will use the `find_by_name` and `read_file` tools to scan their specific `KB` folders before answering your questions, ensuring their responses are grounded in the documents you provide.
