# 📘 FAQ – Knowledge Graph eXchange (KGX)

## ❓ What is KGX?

**KGX (Knowledge Graph eXchange)** is an open-source toolkit for converting and translating knowledge graph models between different platforms and formats — such as Cognite Data Fusion, Neo4j, Azure Digital Twins, and others.

---

## 💡 What problems does KGX solve?

KGX addresses the challenge of **schema interoperability** between different graph-based platforms. While many tools focus on data transformation, KGX focuses on **model translation** — ensuring graph structure, node types, and relationships are preserved when moving between systems.

---

## 🧩 Why does it only support Cognite → Neo4j right now?

This is the **first version** of KGX. The architecture is modular and designed to support other targets and sources like:

- Neo4j → Azure Digital Twins
- Azure Digital Twins → RDF/OWL
- Future support for CSV, SHACL, etc.

The roadmap already includes these.

---

## 🔁 Does KGX migrate data or just the schema?

**Only the data model (schema) for now.**  
KGX is focused on structure: nodes, relationships, and properties.

It does **not** copy instance-level data (like rows or timeseries), which is usually handled by ETL tools or platform-specific SDKs.

---

## 🔎 Why are all nodes labeled as `GraphNode` in Neo4j?

This was an intentional design choice in the MVP for simplicity.

Future versions will support:
- Node labels based on domain types (e.g., `Material`, `Sensor`)
- Configurable mappings per platform or model

---

## 🧪 Is it using a formal schema standard like RDF, SHACL, or OWL?

Not yet. Currently, KGX parses **YAML data models** exported from tools like **Cognite NEAT**, which are widely used but not formally standardized.

A future goal is to **translate between NEAT → RDF → SHACL/OWL** for broader interoperability.

---

## 🖥️ Is there a web interface?

Not yet — KGX is currently **CLI-based**.

However, the roadmap includes a **web UI** for:
- Viewing imported models
- Exporting to various formats
- Interacting with graph schema visually

---

## 🛡️ Are there any security concerns?

Yes — like any CLI tool, it relies on credentials passed through config files or environment variables.

**You should not commit your `config.yaml` with secrets**.  
Use `.gitignore` to exclude it and consider using environment variables or secret managers.

---

## 🤝 Can I contribute?

Absolutely! The project is open source and contributions are welcome.  
Ideas for improvements include:
- Additional platform adapters (e.g., RDF, GraphQL, ADT)
- Web visualization
- Reverse conversion (Neo4j → YAML)

---

## 📄 License?

KGX is licensed under the **MIT License** — you are free to use, modify, and contribute.
