from langchain_core.tools import tool
from pathlib import Path
from datetime import datetime
import subprocess
import shutil


@tool
def write_pdf(latex_content: str) -> str:
    """
    Generate a PDF from a COMPLETE standalone LaTeX document.

    The input must be valid LaTeX and include:

    \\documentclass{article}

    ...

    \\begin{document}

    ...

    \\end{document}

    The input must NOT be wrapped inside markdown code fences.

    Returns:
        Absolute path of the generated PDF.
    """

    # Check for available LaTeX compiler
    compiler = shutil.which("tectonic")

    if compiler is None:
        compiler = shutil.which("pdflatex")

    if compiler is None:
        raise FileNotFoundError(
            "No LaTeX compiler found. Please install Tectonic or MiKTeX (pdflatex)."
        )

    print(f"Using LaTeX compiler: {Path(compiler).stem}")

    # Create output directory if it doesn't exist
    output_dir = Path("output").absolute()
    output_dir.mkdir(exist_ok=True)

    # Create unique filenames using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tex_file = output_dir / f"paper_{timestamp}.tex"
    pdf_file = output_dir / f"paper_{timestamp}.pdf"

    # Write LaTeX content to .tex file
    tex_file.write_text(latex_content, encoding="utf-8")

    # Compile using the detected compiler
    if Path(compiler).stem.lower() == "tectonic":
        result = subprocess.run(
            [
                compiler,
                str(tex_file),
                "-o",
                str(output_dir)
            ],
            capture_output=True,
            text=True
        )
    else:
        result = subprocess.run(
            [
                compiler,
                f"-output-directory={output_dir}",
                str(tex_file)
            ],
            capture_output=True,
            text=True
        )

    # Check for compilation errors
    if result.returncode != 0:
        raise RuntimeError(
            f"LaTeX compilation failed.\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

    # Remove temporary LaTeX files
    for ext in [".aux", ".log", ".out", ".toc"]:
        temp_file = tex_file.with_suffix(ext)
        if temp_file.exists():
            temp_file.unlink()

    # Verify PDF was created
    if not pdf_file.exists():
        raise FileNotFoundError("PDF file was not generated")

    print(f"PDF generated successfully: {pdf_file}")

    return str(pdf_file)

if __name__ == "__main__":

    latex = r"""
\documentclass{article}
\begin{document}
Hello AI Researcher!
\end{document}
"""

    pdf = write_pdf.invoke(
        {
            "latex_content": latex
        }
    )

    print(pdf)