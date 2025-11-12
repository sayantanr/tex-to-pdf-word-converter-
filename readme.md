
---

## 🧾 **README.md**

````markdown
# 📄 Streamlit LaTeX Converter  
> A lightweight Streamlit-based framework to batch convert `.tex` files into **PDF** and **Word (.docx)** — automatically detecting your installed **MiKTeX** and **Pandoc** tools.

---

## 🚀 Overview

This project provides a **simple, GUI-based converter** for LaTeX documents built using **Streamlit**.  
You can either:
- Paste LaTeX code directly into the app, or  
- Enter a folder path to **batch convert** all `.tex` files into both PDF and DOCX formats.

It automatically compiles documents using:
- 🧩 **MiKTeX** (`pdflatex.exe`) for PDF generation  
- 🔁 **Pandoc** (`pandoc.exe`) for Word `.docx` conversion

All outputs (PDFs, DOCXs, and logs) are downloadable directly from the Streamlit interface.

---

## ✨ Features

✅ Converts `.tex` → `.pdf` and `.docx`  
✅ Supports both single-file and bulk directory conversion  
✅ Works with any standard LaTeX code  
✅ Uses local MiKTeX and Pandoc executables — no cloud dependency  
✅ Generates detailed `.log.txt` files for debugging  
✅ 100% offline & privacy-safe  
✅ Cross-platform ready (Windows, Linux, macOS with minor path edits)

---

## 🧠 Requirements

| Component | Purpose | Installation |
|------------|----------|---------------|
| **Python 3.8+** | Core language | [Download](https://www.python.org/downloads/) |
| **Streamlit** | GUI framework | `pip install streamlit` |
| **MiKTeX / TeX Live** | For LaTeX → PDF | [MiKTeX Download](https://miktex.org/download) |
| **Pandoc** | For LaTeX → DOCX | [Pandoc Download](https://pandoc.org/installing.html) |

---

## ⚙️ Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/<your-username>/streamlit-latex-converter.git
   cd streamlit-latex-converter
````

2. Install Python dependencies:

   ```bash
   pip install streamlit
   ```

3. Ensure MiKTeX (`pdflatex.exe`) and Pandoc (`pandoc.exe`) are installed.

4. Open the script and **specify your local paths**:

   ```python
   MIKTEX_PATH = r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe"
   PANDOC_PATH = r"C:\Program Files\Pandoc\pandoc.exe"
   ```

5. Run the app:

   ```bash
   streamlit run latex_converter_app.py
   ```

---

## 🧩 Usage

### 🔹 Mode 1: Paste LaTeX Code

1. Select **📝 Paste LaTeX Code** tab.
2. Paste your LaTeX source.
3. Click **Convert Code**.
4. Download PDF or DOCX directly.

### 🔹 Mode 2: Folder Conversion

1. Select **📂 Convert Directory** tab.
2. Enter full path to your folder (e.g. `C:\Users\Admin\Documents\LatexFiles`).
3. Click **Convert Folder**.
4. Download the resulting ZIP containing all converted files.

---

## 📦 Output Structure

Each processed `.tex` file generates:

```
document.pdf        ← compiled PDF
document.docx       ← converted Word file
document.log.txt    ← compilation logs
```

If multiple files are converted, they’re bundled into a downloadable ZIP archive.

---

## 🧰 Example

**Input LaTeX:**

```latex
\documentclass{article}
\begin{document}
Hello, Sayantan! This is a sample test document.
\end{document}
```

**Generated Outputs:**

* ✅ `document.pdf`
* ✅ `document.docx`
* 🧾 `document.log.txt`

---

## 🧑‍💻 Developer Notes

* If you see “command not found,” update the `MIKTEX_PATH` or `PANDOC_PATH` constants.
* You can verify installation locations by running in Command Prompt:

  ```bash
  where pdflatex
  where pandoc
  ```
* On Linux or macOS, replace `.exe` with your system paths (e.g., `/usr/bin/pdflatex`).

---

## 🧭 Roadmap

* [ ] Inline PDF preview in Streamlit
* [ ] Support for `.bib` bibliography files
* [ ] Option to merge all PDFs into one document
* [ ] Drag-and-drop file upload mode

---

## ⚡ Troubleshooting

| Issue                    | Cause                  | Solution                                      |
| ------------------------ | ---------------------- | --------------------------------------------- |
| `pdflatex.exe not found` | MiKTeX not in PATH     | Edit path manually in the script              |
| Blank PDF or DOCX        | Compilation error      | Check `.log.txt` file for details             |
| Slow conversion          | Large TikZ or images   | Use `--shell-escape` with pdflatex (advanced) |
| Pandoc warning           | Missing LaTeX packages | Install via MiKTeX console automatically      |

---

## 🧑‍🎓 Author

**Sayantan Roy**
Graduate Software Engineer (Cognizant)
💻 Passionate about AI, automation, and intelligent document systems.
🌐 [LinkedIn](https://linkedin.com) • [GitHub](https://github.com/your-username)

---

## 🪪 License

This project is licensed under the **MIT License** — you’re free to use, modify, and distribute it with attribution.

```
MIT License © 2025 Sayantan Roy
```

---

## 🌟 Acknowledgements

* [Streamlit](https://streamlit.io) for the intuitive UI framework.
* [MiKTeX](https://miktex.org) & [Pandoc](https://pandoc.org) for seamless document conversion.
* The open-source LaTeX community for decades of excellence in scientific publishing.

---

## 💡 Tip

To make this app start instantly on Windows:

* Create a batch file `run_latex_converter.bat`:

  ```bat
  @echo off
  streamlit run "C:\Users\Admin\latex_converter_app.py"
  ```
* Double-click it anytime to launch the GUI.

---

⭐ If you found this project useful, please give it a **star** on GitHub!

```


```
