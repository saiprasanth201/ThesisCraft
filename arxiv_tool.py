# import requests


# def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
#     """
# Search arXiv for recently published papers on a given topic.

# Args:
#     topic (str): Topic to search for.
#     max_results (int): Maximum number of papers to retrieve.

# Returns:
#     dict: Parsed arXiv response containing paper metadata.
# """
#     topic = topic.strip().replace( '"'," ")  
#     query = f'"{topic}"'
#     for char in "()":
#         if char in topic:
#             print(f"Invalid character '{char}' found in topic.")
#             raise ValueError(f"Topic cannot contain '{char}'.")
#     url = (
#         "https://export.arxiv.org/api/query"
#         f"?search_query=all:{query}"
#         f"&max_results={max_results}"
#         "&sortBy=submittedDate"
#         "&sortOrder=descending"
#     )
    
#     print(f"Making request to arxiv API :{url}")
#     resp = requests.get(url,timeout=10, headers={"User-Agent": "AI-Researcher/1.0 (LangGraph + Ollama)"})

#     if not resp.ok:
#         print(f"ArXiv API request failed: {resp.status_code} - {resp.text}")
#         raise ValueError(f"Bad response from arXiv API: {resp}\n{resp.text}")

#     data = parse_arxiv_xml(resp.text)
#     return data 

#     # print("Status code:", resp.status_code)
#     # print("Status text:", resp.text)

#     # return {
#     #     "status_code": resp.status_code,
#     #     "response": resp.text
#     # }

# #parse the xml content from arxiv API response
# import xml.etree.ElementTree as ET
# def parse_arxiv_xml(xml_content:str)-> dict:
#     """ should parse xml content form arxiv API response. """

#     entries = []
#     ns = {
#         "atom": "http://www.w3.org/2005/Atom",
#         "arxiv": "http://arxiv.org/schemas/atom"
#     }
#     root = ET.fromstring(xml_content)
# # Loop through each <entry> in Atom namespace
#     for entry in root.findall("atom:entry", ns):
# # Extract authors
#         authors = [
#             author. findtext("atom:name", namespaces=ns)
#             for author in entry.findall("atom:author", ns)
#         ]
# # Extract categories (term attribute)
#         categories = [
#             cat.attrib.get("term")
#             for cat in entry. findall("atom:category", ns)
#         ]
# #extract pdf link (rel="related" and type="application/pdf")
#         pdf_link = None
#         for link in entry.findall("atom:link", ns):
#             if link.attrib.get("rel") == "related" and link.attrib.get("type") == "application/pdf":
#                 pdf_link = link.attrib.get("href")
#                 break

#         entries.append({
#             "title": entry.findtext("atom:title", namespaces=ns),
#             "summary": entry.findtext("atom:summary", namespaces=ns),
#             "published": entry.findtext("atom:published", namespaces=ns),
#             "updated": entry.findtext("atom:updated", namespaces=ns),
#             "authors": authors,
#             "categories": categories,
#             "pdf_link": pdf_link
#         })

#     return {"entries": entries}

# #convert the functionalty into tool 
# from langchain.tools import tool

# @tool
# def arxiv_search(topic: str) -> list[dict]:
#     """Search for recently uploaded papers on arXiv based on a topic
#     Args:
#        topic : the topic to search for papers about on arXiv
#     Returns:
#         A list of papers with their metadata including title, summary, authors, categories, and PDF link,etc.
#     """
#     print("ArXiv Agent Called")
#     print(f"Searching for ArXiv papers on topic: {topic}")
#     papers = search_arxiv_papers(topic)
#     if len(papers["entries"]) == 0:
#         print(f"No papers found for topic: {topic}")

#     return [
#         {
#             "title": "No papers found",
#             "published": "",
#             "pdf_link": ""
#         }
#     ]
#     print(f"Found {len(papers['entries'])} papers for topic: {topic}")
#     return [
#     {
#         "title": p["title"],
#         "published": p["published"],
#         "pdf_link": p["pdf_link"],
#     }
#     for p in papers["entries"]
# ]

import re
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from langchain.tools import tool


def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
    """
    Search arXiv for recent papers related to a topic across Computer Science/AI categories.
    """
    # 1. Clean out problematic characters without breaking phrases
    cleaned_topic = re.sub(r'[\(\)"\']', " ", topic).strip()

    words = [
        w for w in cleaned_topic.split()
        if w.upper() not in ["AND", "OR"]
    ]
    search_phrase = " ".join(words)

    # 2. Target CS/AI categories without forcing literal double quotes
    query = f"(cat:cs.CL OR cat:cs.AI OR cat:cs.LG) AND all:{search_phrase}"
    encoded_query = urllib.parse.quote(query)

    url = (
        "https://export.arxiv.org/api/query"
        f"?search_query={encoded_query}"
        f"&max_results={max_results}"
        "&sortBy=submittedDate"
        "&sortOrder=descending"
    )

    print(f"Making request to arXiv API: {url}")

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "AI-Researcher/1.0"
        }
    )

    if not response.ok:
        raise ValueError(
            f"Bad response from arXiv API: {response.status_code}"
        )

    return parse_arxiv_xml(response.text)


def parse_arxiv_xml(xml_content: str) -> dict:
    entries = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }

    root = ET.fromstring(xml_content)

    for entry in root.findall("atom:entry", ns):
        authors = [
            author.findtext("atom:name", namespaces=ns)
            for author in entry.findall("atom:author", ns)
        ]

        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if (
                link.attrib.get("title") == "pdf"
                or link.attrib.get("type") == "application/pdf"
            ):
                pdf_link = link.attrib["href"]
                break

        # Clean newlines out of titles and summaries
        title = " ".join(entry.findtext("atom:title", namespaces=ns).split())
        summary = " ".join(entry.findtext("atom:summary", namespaces=ns).split())

        entries.append(
            {
                "title": title,
                "summary": summary,
                "published": entry.findtext("atom:published", namespaces=ns),
                "authors": authors,
                "pdf_link": pdf_link,
            }
        )

    return {"entries": entries}


@tool
def arxiv_search(topic: str) -> list[dict]:
    """
    Search arXiv for recent papers on a research topic.

    Returns titles, authors, publication date, abstract summary, and PDF link.
    """
    print("ArXiv Agent Called")
    print(f"Searching for ArXiv papers on topic: {topic}")

    papers = search_arxiv_papers(topic)

    if not papers["entries"]:
        return []

    print(f"Found {len(papers['entries'])} papers.")

    # Included authors & summary so the LLM can present paper details
    return [
        {
            "title": p["title"],
            "authors": p["authors"][:3],  # First 3 authors
            "summary": p["summary"][:300] + "...",  # Concise snippet
            "published": p["published"][:10],  # YYYY-MM-DD
            "pdf_link": p["pdf_link"],
        }
        for p in papers["entries"]
    ]