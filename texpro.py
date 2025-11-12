#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit App: Professional LaTeX (.tex) → PDF and DOCX Converter
Includes:
✅ Inline PDF Viewer
✅ Error Line Extraction
✅ Drag-and-Drop Upload
✅ Configurable Paths & Flags
"""

import streamlit as st
import subprocess
import tempfile
import zipfile
import io
import os
from pathlib import Path
import base64
import re

# ============================================================
# 1️⃣ SESSION CONFIG (save settings persistently during runtime)
# ============================================================
if "miktex_path" not in st.session_state:
    st.session_state.miktex_path = r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe"
if "pandoc_path" not in st.session_state:
    st.session_state.pandoc_path = r"C:\Program Files\Pandoc\pandoc.exe"
if "pdflatex_flags" not in st.session_state:
    st.session_state.pdflatex_flags = "-interaction=nonstopmode -halt-on-error"

# ============================================================
# 2️⃣ UTILITY FUNCTIONS
# ============================================================

def run_command(cmd, cwd, timeout=120):
    try:
        proc = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        out = proc.stdout.decode(errors="ignore")
        err = proc.stderr.decode(errors="ignore")
        return proc.returncode == 0, out, err
    except subprocess.TimeoutExpired:
        return False, "", "❌ Timeout expired."
    except Exception as e:
        return False, "", f"❌ Exception: {e}"

def extract_latex_error(log_text):
    """Extract key LaTeX error lines for user clarity."""
    match = re.search(r"! (.*?)\n", log_text)
    if match:
        return f"❌ **Error:** {match.group(1)}"
    else:
        return "✅ No critical LaTeX error found."

def compile_latex(tex_code, filename="document.tex", make_pdf=True, make_docx=True):
    """Compile LaTeX to PDF/DOCX and return results + logs."""
    results = {"pdf": None, "docx": None, "log": "", "error_summary": ""}
    with tempfile.TemporaryDirectory() as tmp:
        tex_path = Path(tmp) / filename
        tex_path.write_text(tex_code, encoding="utf-8")

        # --- PDF
        if make_pdf:
            flags = st.session_state.pdflatex_flags.split()
            cmd_pdf = [st.session_state.miktex_path] + flags + [filename]
            ok, out, err = run_command(cmd_pdf, tmp)
            results["log"] += f"\n--- pdflatex log ---\n{out}\n{err}\n"
            pdf_path = tex_path.with_suffix(".pdf")
            if ok and pdf_path.exists():
                results["pdf"] = pdf_path.read_bytes()
            else:
                results["error_summary"] = extract_latex_error(out + err)

        # --- DOCX
        if make_docx:
            cmd_docx = [st.session_state.pandoc_path, filename, "-o", tex_path.with_suffix(".docx").name]
            ok, out, err = run_command(cmd_docx, tmp)
            results["log"] += f"\n--- pandoc log ---\n{out}\n{err}\n"
            docx_path = tex_path.with_suffix(".docx")
            if ok and docx_path.exists():
                results["docx"] = docx_path.read_bytes()

    return results


def convert_directory(path, make_pdf=True, make_docx=True):
    """Convert all .tex files in directory."""
    zip_out = io.BytesIO()
    path = Path(path)
    tex_files = list(path.glob("*.tex"))
    if not tex_files:
        raise FileNotFoundError("No .tex files found in folder.")
    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as zout:
        for tex_file in tex_files:
            code = tex_file.read_text(encoding="utf-8", errors="ignore")
            res = compile_latex(code, tex_file.name, make_pdf, make_docx)
            base = tex_file.stem
            if res["pdf"]:
                zout.writestr(f"{base}.pdf", res["pdf"])
            if res["docx"]:
                zout.writestr(f"{base}.docx", res["docx"])
            zout.writestr(f"{base}.log.txt", res["log"])
    zip_out.seek(0)
    return zip_out

def show_pdf_inline(pdf_bytes):
    """Embed PDF directly in Streamlit."""
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600px"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# ============================================================
# 3️⃣ STREAMLIT UI
# ============================================================
st.set_page_config(page_title="LaTeX to PDF/DOCX Pro", layout="wide")
st.title("📄 LaTeX → PDF / DOCX Professional Converter")

tabs = st.tabs(["📝 Paste LaTeX Code", "📂 Upload Files", "⚙️ Configuration"])

# ============================================================
# 📝 TAB 1 — Direct Code Input
# ============================================================
with tabs[0]:
    st.subheader("Direct LaTeX Input")
    tex_code = st.text_area("Paste LaTeX code:", height=300, placeholder="\\documentclass{article}\n\\begin{document}\nHello World!\n\\end{document}")
    filename = st.text_input("Filename", "document.tex")

    if st.button("Convert"):
        if not tex_code.strip():
            st.warning("Please enter LaTeX code.")
        else:
            result = compile_latex(tex_code, filename)
            if result["pdf"]:
                st.success("✅ PDF generated successfully.")
                st.download_button("⬇️ Download PDF", result["pdf"], filename.replace(".tex", ".pdf"), "application/pdf")
                show_pdf_inline(result["pdf"])
            if result["docx"]:
                st.download_button("⬇️ Download DOCX", result["docx"], filename.replace(".tex", ".docx"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.info(result["error_summary"])
            st.text_area("Log Output", result["log"], height=200)

# ============================================================
# 📂 TAB 2 — Drag-and-Drop Upload
# ============================================================
with tabs[1]:
    st.subheader("Upload .tex Files for Batch Conversion")
    uploaded_files = st.file_uploader("Upload one or more .tex files", type=["tex"], accept_multiple_files=True)

    if uploaded_files:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zout:
            for uploaded in uploaded_files:
                tex_code = uploaded.read().decode("utf-8", errors="ignore")
                result = compile_latex(tex_code, uploaded.name)
                if result["pdf"]:
                    zout.writestr(uploaded.name.replace(".tex", ".pdf"), result["pdf"])
                if result["docx"]:
                    zout.writestr(uploaded.name.replace(".tex", ".docx"), result["docx"])
                zout.writestr(uploaded.name.replace(".tex", ".log.txt"), result["log"])
        zip_buffer.seek(0)
        st.success("✅ All files processed successfully.")
        st.download_button("⬇️ Download All (ZIP)", zip_buffer, file_name="converted_files.zip", mime="application/zip")

# ============================================================
# ⚙️ TAB 3 — Configuration
# ============================================================
with tabs[2]:
    st.subheader("Tool Configuration")

    st.text("Set full paths to your installed tools:")
    st.session_state.miktex_path = st.text_input("MiKTeX (pdflatex.exe)", st.session_state.miktex_path)
    st.session_state.pandoc_path = st.text_input("Pandoc (pandoc.exe)", st.session_state.pandoc_path)
    st.session_state.pdflatex_flags = st.text_input("pdflatex Flags", st.session_state.pdflatex_flags)

    if st.button("Verify Paths"):
        mik_exists = os.path.isfile(st.session_state.miktex_path)
        pand_exists = os.path.isfile(st.session_state.pandoc_path)
        col1, col2 = st.columns(2)
        col1.success(f"MiKTeX: {'✅ Found' if mik_exists else '❌ Not Found'}")
        col2.success(f"Pandoc: {'✅ Found' if pand_exists else '❌ Not Found'}")

    st.caption("All settings persist only for this session.")
