from langchain_core.tools import tool
import io
import PyPDF2
import requests

@tool
def read_pdf_from_url(url: str) -> str:
    """
    Reads a PDF from the given URL and extracts its text content.

    Args:
        url (str): The URL of the PDF file.

    Returns:
        str: The extracted text content from the PDF.
    """

    #access pdf via URL
    response = requests.get(url, timeout=10)
    if not response.ok:
        raise ValueError(
            f"Failed to download PDF: {response.status_code}"
        )
    # print(response.status_code)
    pdf_file = io.BytesIO(response.content)
    # print (pdf_file)

    #retrive the text from the pdf
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    print(len(pdf_reader.pages))

    #extract text from all pages
    text = ""
    for i, page in enumerate(pdf_reader.pages):
        page_text = page.extract_text()

        if page_text:
            print("=" * 80)
            print(f"Page {i+1}/{len(pdf_reader.pages)}")
            print("=" * 80)
            print(page_text[:300])
            print()

            text += page_text + "\n"
        else:
            print("=" * 80)
            print(f"Page {i+1}/{len(pdf_reader.pages)}")
            print("=" * 80)
            print("No text found on this page.")
            print("=" * 80)
            print()

    print(f"Successfully extracted text length: {len(text)} characters")
    return text.strip()

if __name__ == "__main__":
    url = "https://arxiv.org/pdf/2306.16913.pdf"

    result = read_pdf_from_url.invoke({"url": url})

    print(result[:1000])
    
    