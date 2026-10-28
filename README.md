# Clarity — Understand More. Read Less.

**Clarity** is a Python-based document summarization application that helps make lengthy documents easier to understand and review. It extracts important information and presents it through summaries, key points, and a visual mind map of key concepts.

The goal is simple: spend less time navigating lengthy documents and more time understanding what matters.

## ✨ Features

- **Document Upload:** Work with supported PDF, DOCX, and TXT documents.
- **Text Summarization:** Generate summaries using LexRank-based extractive summarization.
- **Key Point Extraction:** Identify important sentences and information from a document.
- **Keyword Extraction:** Discover relevant phrases and concepts using YAKE.
- **Concept Exploration:** Use NLP techniques to identify useful noun phrases and concepts.
- **Visual Mind Map:** Explore document concepts and their explanations through a graphical overview.
- **Interactive Interface:** Access the application's features through a Streamlit web interface.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| Sumy and LexRank | Extractive text summarization |
| spaCy | Natural language processing |
| YAKE | Keyword extraction |
| PyPDF | PDF text extraction |
| python-docx | Word document processing |
| scikit-learn | Machine learning and text-analysis utilities |
| Graphviz | Concept-map visualization, if used by the current implementation |

## 📸 Application Preview

<img width="1908" height="964" alt="image" src="https://github.com/user-attachments/assets/24f9f93a-1c8e-4edc-bc06-ae0604a2479f" />
<img width="1336" height="440" alt="image" src="https://github.com/user-attachments/assets/34dcb626-e855-420c-b591-1af0ae0369f9" />
<img width="1138" height="210" alt="image" src="https://github.com/user-attachments/assets/c8317c51-d281-4b90-a6b4-fd9aee801f1a" />
<img width="1265" height="538" alt="image" src="https://github.com/user-attachments/assets/5f651ed6-4677-4ce1-9bdf-16e58963b2a3" />
<img width="1160" height="915" alt="image" src="https://github.com/user-attachments/assets/60fb0b07-5f98-45cc-a53a-1bc029e407df" />
<img width="1204" height="953" alt="image" src="https://github.com/user-attachments/assets/b82d5e3e-78d5-43f2-82cd-20f946c64047" />

## 🚀 Getting Started

### Prerequisites

- Python installed on your computer
- pip, Python's package installer
- Git, if you want to clone the repository

### 1. Clone the repository

```bash
git clone https://github.com/Tisha-Mittal/Clarity.git
cd Clarity
```

### 2. Open the backend folder

```bash
cd Backend
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

Once `Backend/requirements.txt` has been added:

```bash
pip install -r requirements.txt
```

Install the English language model required by spaCy:

```bash
python -m spacy download en_core_web_sm
```

### 5. Run Clarity

```bash
streamlit run app.py
```

Streamlit will provide a local URL that you can open in your browser.

## 📂 Project Structure

```text
Clarity/
├── .gitignore
├── README.md
└── Backend/
    ├── .gitignore
    ├── app.py
    └── requirements.txt
```

*This structure represents the intended layout; additional files may be present in your repository.*

## 🔮 Future Improvements

- Locally running language models for abstractive summarization
- Topic-wise summaries with clearer section headings
- Improved handling of long documents
- More informative concept relationships in the mind map
- Additional document-analysis features

## 🎯 Project Objective

Clarity is a learning project focused on exploring Python, natural language processing, document processing, and interactive application development.

The project aims to make information easier to navigate, understand, and revise through a combination of text-based and visual tools.

---

**Clarity — Understand More. Read Less.**
