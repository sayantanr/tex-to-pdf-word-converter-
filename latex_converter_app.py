#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit App: Convert LaTeX (.tex) → PDF and DOCX
Manually specifies MiKTeX (pdflatex.exe) and Pandoc executable paths.
"""

import streamlit as st
import subprocess
import tempfile
import zipfile
import io
import os
from pathlib import Path

# ============================================================
# 1️⃣ SPECIFY YOUR INSTALLATION PATHS HERE
# ============================================================

# 👇👇  EDIT THESE LINES ACCORDING TO YOUR SYSTEM  👇👇
MIKTEX_PATH = r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe"
PANDOC_PATH = r"C:\Program Files\Pandoc\pandoc.exe"
# 👆👆  KEEP the .exe filenames and full paths  👆👆

# ============================================================
# 2️⃣ Utility Functions
# ============================================================
def check_file_exists(path: str) -> bool:
    return os.path.isfile(path)

def run_command(cmd, cwd, timeout=120):
    """Run a command and return (success, stdout, stderr)."""
    try:
        proc = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        out = proc.stdout.decode(errors="ignore")
        err = proc.stderr.decode(errors="ignore")
        return proc.returncode == 0, out, err
    except subprocess.TimeoutExpired:
        return False, "", "❌ Timeout expired."
    except Exception as e:
        return False, "", f"❌ Exception: {e}"

def compile_latex(tex_code: str, filename="document.tex", make_pdf=True, make_docx=True):
    """Compile LaTeX code into PDF and DOCX using given tools."""
    results = {"pdf": None, "docx": None, "log": ""}
    with tempfile.TemporaryDirectory() as tmp:
        tex_path = Path(tmp) / filename
        tex_path.write_text(tex_code, encoding="utf-8")

        # PDF using MiKTeX
        if make_pdf:
            cmd_pdf = [MIKTEX_PATH, "-interaction=nonstopmode", "-halt-on-error", filename]
            ok, out, err = run_command(cmd_pdf, tmp)
            results["log"] += f"\n--- pdflatex log ---\n{out}\n{err}\n"
            pdf_file = tex_path.with_suffix(".pdf")
            if ok and pdf_file.exists():
                results["pdf"] = pdf_file.read_bytes()

        # DOCX using Pandoc
        if make_docx:
            docx_file = tex_path.with_suffix(".docx")
            cmd_docx = [PANDOC_PATH, filename, "-o", docx_file.name]
            ok, out, err = run_command(cmd_docx, tmp)
            results["log"] += f"\n--- pandoc log ---\n{out}\n{err}\n"
            if ok and docx_file.exists():
                results["docx"] = docx_file.read_bytes()

    return results


def convert_directory(folder_path: str, make_pdf=True, make_docx=True):
    """Convert all .tex files in a directory to PDF/DOCX."""
    output_zip = io.BytesIO()
    folder = Path(folder_path)
    tex_files = list(folder.glob("*.tex"))
    if not tex_files:
        raise FileNotFoundError("No .tex files found in directory!")

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zout:
        for tex_file in tex_files:
            code = tex_file.read_text(encoding="utf-8", errors="ignore")
            result = compile_latex(code, tex_file.name, make_pdf, make_docx)
            base = tex_file.stem
            if result["pdf"]:
                zout.writestr(f"{base}.pdf", result["pdf"])
            if result["docx"]:
                zout.writestr(f"{base}.docx", result["docx"])
            zout.writestr(f"{base}.log.txt", result["log"])
    output_zip.seek(0)
    return output_zip


# ============================================================
# 3️⃣ Streamlit UI
# ============================================================
st.set_page_config(page_title="LaTeX → PDF/DOCX Converter", layout="centered")
st.title("📄 LaTeX (.tex) to PDF / Word Converter")

# --- Tool detection ---
mik_ok = check_file_exists(MIKTEX_PATH)
pand_ok = check_file_exists(PANDOC_PATH)

col1, col2 = st.columns(2)
col1.info(f"MiKTeX (pdflatex.exe): {'✅ Found' if mik_ok else '❌ Missing'}")
col2.info(f"Pandoc (pandoc.exe): {'✅ Found' if pand_ok else '❌ Missing'}")

if not (mik_ok or pand_ok):
    st.error("Neither MiKTeX nor Pandoc were found at the specified paths. Please check the paths in your code.")
    st.stop()

# Tabs for modes
tab1, tab2 = st.tabs(["📝 Paste LaTeX Code", "📂 Convert Directory"])

# ============================================================
# TAB 1: Direct .tex input
# ============================================================
with tab1:
    st.subheader("Enter LaTeX code:")
    tex_code = st.text_area(
        "Paste your LaTeX source here:",
        height=300,
        placeholder="\\documentclass{article}\n\\begin{document}\nHello Sayantan!\n\\end{document}"
    )
    filename = st.text_input("Filename (optional)", "document.tex")

    if st.button("Convert Code"):
        if not tex_code.strip():
            st.warning("Please paste your LaTeX code first.")
        else:
            result = compile_latex(tex_code, filename, make_pdf=mik_ok, make_docx=pand_ok)
            if result["pdf"]:
                st.download_button("⬇️ Download PDF", data=result["pdf"], file_name=filename.replace(".tex", ".pdf"), mime="application/pdf")
            if result["docx"]:
                st.download_button("⬇️ Download DOCX", data=result["docx"], file_name=filename.replace(".tex", ".docx"), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.text_area("Compilation Log", result["log"], height=200)

# ============================================================
# TAB 2: Convert all .tex in a folder
# ============================================================
with tab2:
    st.subheader("Enter full folder path:")
    folder = st.text_input("Example: C:\\Users\\Admin\\Documents\\LatexProjects")

    if st.button("Convert Folder"):
        if not folder or not os.path.isdir(folder):
            st.error("Invalid folder path.")
        else:
            with st.spinner("Processing all .tex files..."):
                try:
                    zip_out = convert_directory(folder, make_pdf=mik_ok, make_docx=pand_ok)
                    st.success("✅ Conversion complete!")
                    st.download_button("⬇️ Download Results ZIP", data=zip_out, file_name="converted_latex.zip", mime="application/zip")
                except Exception as e:
                    st.error(f"Error: {e}")
