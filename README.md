# ThesisCraft

> An AI-powered research assistant that automates academic paper discovery, analysis, summarization, and research paper generation using Large Language Models.

ThesisCraft enables researchers to discover the latest papers from arXiv, analyze research PDFs, generate concise summaries, identify future research directions, and automatically produce a LaTeX research paper that can be compiled into a PDF.

---

## Features

- Search the latest research papers from arXiv
- Download and analyze research papers directly from PDF URLs
- Summarize research papers using LLMs
- Generate future research ideas inspired by existing work
- Automatically generate complete research papers in LaTeX
- Export generated papers as PDF
- Interactive multi-turn research workflow
- Powered by LangChain, LangGraph, Groq/Ollama, and arXiv

---

## Tech Stack

### AI & LLM Frameworks

- LangChain
- LangGraph
- Ollama
- Groq
- Qwen 3
- Llama 3.1

### APIs

- arXiv API

### Python Libraries

- Requests
- PyPDF2
- python-dotenv

### Document Processing

- LaTeX
- PDFLaTeX / Tectonic

---

## Project Architecture

```text
                    User
                      │
                      ▼
            AI Research Assistant
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
    arXiv Search   PDF Reader   PDF Generator
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
           Research Analysis Engine
                      │
                      ▼
       Research Ideas & LaTeX Generation
                      │
                      ▼
             Generated Research PDF
```

---

## Workflow

1. User provides a research topic.
2. The agent searches arXiv for the latest research papers.
3. Relevant papers are presented to the user.
4. The selected paper is downloaded and analyzed.
5. The agent summarizes the paper.
6. Future research directions are generated.
7. A complete research paper is written in LaTeX.
8. The LaTeX document is compiled into a PDF.

---

## Project Structure

```text
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

### Clone the repository

```bash
git clone https://github.com/saiprasanth201/ThesisCraft.git
```

### Navigate into the project

```bash
cd ThesisCraft
```

### Install dependencies

```bash
uv sync
```

### Start Ollama

```bash
ollama serve
```

### Download the Qwen model

```bash
ollama pull qwen3:latest
```

### Run the application

```bash
uv run ai_researcher.py
```

---

## Example Workflow

```text
User
│
├── Research Retrieval-Augmented Generation (RAG)
│
▼
Search latest arXiv papers
│
▼
Select a research paper
│
▼
Analyze the PDF
│
▼
Generate summary
│
▼
Suggest future research ideas
│
▼
Generate a novel research paper
│
▼
Export the paper as PDF
```

---

## Current Status

### Implemented

- arXiv paper search
- PDF downloading and parsing
- Research paper summarization
- Future research idea generation
- LaTeX research paper generation
- PDF compilation
- Interactive CLI workflow

### In Progress

- Streamlit web interface
- Better conversation memory
- Improved search relevance
- Paper recommendation system
- Enhanced LaTeX formatting

---

## Future Roadmap

- Retrieval-Augmented Generation (RAG)
- ChromaDB integration
- FAISS vector search
- Multi-agent research workflow
- Automatic citation management
- Literature review generation
- Research memory
- Streamlit dashboard
- Research history management
- IEEE/ACM paper templates

---

## Author

**Sai Prasanth**

B.Tech Computer Science Engineering

SRM University AP

GitHub: https://github.com/saiprasanth201

---

## License

This project is intended for educational and research purposes.