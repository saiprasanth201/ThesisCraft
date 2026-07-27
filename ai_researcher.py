# from langchain_ollama import ChatOllama
# from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from arxiv_tool import arxiv_search
from write_pdf import write_pdf
from read_pdf import read_pdf_from_url
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()


tools = [arxiv_search, write_pdf, read_pdf_from_url]
model = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"),temperature=0)
# model = ChatOllama(model="qwen3:latest",temperature=0)
graph = create_agent(model=model,tools=tools)

INITIAL_PROMPT ="""
You are an expert researcher in the fields of physics, mathematics,
computer science, quantitative biology, quantitative finance, statistics,
electrical engineering and systems science, and economics.

You are going to analyze recent research papers in one of these fields in
order to identify promising new research directions and then write a new
research paper. For research information or getting papers, For research information, use the arxiv_search tool.

You are an expert AI Research Assistant.
When you receive paper search results from the `arxiv_search` tool:
1. ALWAYS present a numbered list containing the Title, Authors, Published Date, and a brief 1-2 sentence Summary of EACH returned paper.
2. Never ask the user to pick a paper without first displaying the list of choices.
3. Once listed, ask the user which paper they would like to inspect or read using `read_pdf`.

IMPORTANT:

1. If the user's research topic is specific and unambiguous, immediately call arxiv_search.

2. If the user's request is ambiguous (for example "RAG", "Transformers", "GAN", etc.), first ask ONE clarification question.

3. Do NOT call arxiv_search until the user has clarified the topic.

4. After the topic is clear, call arxiv_search exactly once.
You will use the tools provided to search for papers, read them, and write a new
paper based on the ideas you find.

To start with, have a conversation with me in order to figure out what topic
to research. Then tell me about some recently published papers with that topic.
Once I've decided which paper I'm interested in, go ahead and read it in order
to understand the research that was done and the outcomes.

Pay particular attention to the ideas for future research and think carefully
about them, then come up with a few ideas. Let me know what they are and I'll
decide what one you should write a paper about.

If the user asks to write a research paper,
you MUST do ALL of the following:

1. Write a COMPLETE standalone LaTeX document.

2. The LaTeX document MUST contain:

- Title
- Authors
- Abstract
- Keywords
- Introduction
- Related Work
- Methodology
- Mathematical Equations where appropriate
- Experimental Results
- Future Work
- Conclusion
- References

3. Return ONLY valid LaTeX.

4. Immediately call the write_pdf tool using the generated LaTeX.

5. Never ask the user for confirmation.

6. Never stop after generating the LaTeX.

7. Never explain the paper instead of writing it."""

# def print_stream(stream):
#     for s in stream:
#         message = s["messages"][-1]
#         print(f"Message received: {message.content[:200]}...")
#         message.pretty_print()

# while True:
#     user_input = input("User: ")
#     if user_input:
#         messages = [
#                     {"role": "system", "content": INITIAL_PROMPT},
#                     {"role": "user", "content": user_input}
#                 ]
#         input_data = {
#             "messages" : messages
#         }
#         print_stream(graph.stream(input_data, stream_mode="values"))


def print_stream(stream):
    for s in stream:
        if "messages" in s and s["messages"]:
            message = s["messages"][-1]
            message.pretty_print()

# 3. Maintain state across iterations
chat_history = [SystemMessage(content=INITIAL_PROMPT)]

print("--- AI Researcher Initialized (Type 'exit' to quit) ---")

while True:
    user_input = input("\nUser: ").strip()
    
    if user_input.lower() in ["exit", "quit"]:
        print("Ending session.")
        break

    if user_input:
        # Append user message to history
        chat_history.append(HumanMessage(content=user_input))
        
        input_data = {"messages": chat_history}
        
        # Stream response
        try:
          for chunk in graph.stream(input_data, stream_mode="values"):
            if "messages" in chunk:
                chat_history = chunk["messages"]

        except Exception as e:
            print(f"\nError: {e}")
            continue
                
        # Print only the latest response from the model/tool
        if chat_history:
            chat_history[-1].pretty_print()
