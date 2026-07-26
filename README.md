# ThesisCraft

An AI-powered research assistant that automates academic paper discovery, PDF analysis, literature summarization, and research paper generation using LangGraph, LangChain, Ollama, and the arXiv API.

---

## Features

- Search the latest research papers from arXiv
- Read PDF papers directly from arXiv URLs
- Analyze and summarize research papers
- Suggest future research directions
- Generate research papers in LaTeX
- Export generated papers as PDF
- Powered by local LLMs using Ollama (Qwen 3)

---

## Tech Stack

### AI Frameworks

- LangChain
- LangGraph
- Ollama
- Qwen 3

### APIs

- arXiv API

### Python Libraries

- Requests
- PyPDF2
- python-dotenv

### Document Generation

- LaTeX
- PDF

---

## Project Architecture

```

User
│
▼
LangGraph ReAct Agent
│
├──────────────► arXiv Search Tool
│
├──────────────► PDF Reader Tool
│
└──────────────► PDF Writer Tool
│
▼
Generated Research Paper

```

---

## Project Workflow

1. User provides a research topic.
2. Agent searches arXiv for the latest papers.
3. User selects a paper.
4. Agent downloads and reads the paper.
5. Agent summarizes the research.
6. Agent suggests future research ideas.
7. Agent generates a research paper.
8. Paper is rendered into a PDF.

---

## Folder Structure

```

ThesisCraft/
│
├── ai_researcher.py
├── arxiv_tool.py
├── read_pdf.py
├── write_pdf.py
├── output/
├── pyproject.toml
├── uv.lock
└── README.md

```

---

## Installation

Clone the repository

```bash
git clone https://github.com/saiprasanth201/ThesisCraft.git
```

Move into the project

```bash
cd ThesisCraft
```

Install dependencies

```bash
uv sync
```

Start Ollama

```bash
ollama serve
```

Download Qwen 3

```bash
ollama pull qwen3:latest
```

Run the project

```bash
uv run ai_researcher.py
```

---

## Example

```

User:
Research Large Language Models

↓

Agent searches arXiv

↓

Returns latest papers

↓

Reads selected paper

↓

Summarizes findings

↓

Generates research paper

↓

Exports PDF

```

---

## Future Improvements

- RAG-based paper retrieval
- ChromaDB integration
- FAISS vector search
- Multi-Agent research workflow
- Citation generation
- Automatic literature review
- Research memory
- Streamlit Web Interface

---

## Author

Sai Prasanth

B.Tech Computer Science Engineering

SRM University AP

GitHub:
https://github.com/saiprasanth201
