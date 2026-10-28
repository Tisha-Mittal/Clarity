import math
import streamlit as st
from pypdf import PdfReader
from docx import Document
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import yake
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import NMF


# -------------------------------
# 1. Page configuration
# -------------------------------

st.set_page_config(
    page_title="Clarity | Document Summariser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -------------------------------
# 2. Custom styling
# -------------------------------


# -------------------------------
# 2. Custom styling
# -------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700;800&display=swap');

    :root {
        --ink: #2b211b;
        --espresso: #39291f;
        --walnut: #59402f;
        --cocoa: #785a43;
        --taupe: #8d7b6b;
        --gold: #aa854b;
        --gold-light: #d1b47a;
        --gold-pale: #eadcc1;
        --parchment: #f3ebdf;
        --cream: #faf6ee;
        --ivory: #fffdf8;
        --line: #e4d8c7;
        --soft-shadow: #39291f12;
    }

    /* ===== Page background ===== */
    

/* ===== Soft ivory background ===== */

.stApp {
    background:
        radial-gradient(
            ellipse at 8% 8%,
            rgba(255, 253, 247, 0.98) 0%,
            transparent 45%
        ),
        radial-gradient(
            ellipse at 95% 90%,
            rgba(221, 197, 161, 0.22) 0%,
            transparent 40%
        ),
        #f4ede2;

    background-attachment: fixed;
    color: #2b211b;
    font-family: 'DM Sans', sans-serif;
}
    .block-container {
        max-width: 1080px;
        padding-top: 2.3rem;
        padding-bottom: 3.5rem;
    }

    /* ===== Typography ===== */
    h1, h2, h3 {
        color: var(--ink) !important;
        font-family: 'Playfair Display', Georgia, serif !important;
    }

    p {
        color: var(--walnut);
    }

    label {
        color: var(--espresso) !important;
        font-weight: 600 !important;
    }

    /* ===== Brand ===== */
    .brand {
        font-family: 'Manrope', sans-serif;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 3.5px;
        color: var(--walnut);
        margin-bottom: 24px;
    }

    /* ===== Hero / introduction ===== */
    .hero {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(
                120deg,
                #fffdf8 0%,
                #f7efe2 58%,
                #eee0ca 100%
            );
        padding: 43px 40px 38px;
        border: 1px solid #dfceb4;
        border-radius: 5px 22px 22px 22px;
        margin-bottom: 34px;
        box-shadow:
            0 16px 42px #39291f0b,
            inset 0 1px 0 #ffffff;
    }

    .hero::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(
            180deg,
            #d8bd83,
            #a17a40,
            #6c4c32
        );
    }

    .hero-label {
        display: inline-block;
        background: #efe3ce;
        color: #785a35;
        border: 1px solid #ddc9a6;
        padding: 7px 12px;
        border-radius: 3px;
        font-family: 'Manrope', sans-serif;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 17px;
    }

    .hero h1 {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 43px;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -1px;
        margin: 0 0 15px;
        color: #2b211b !important;
    }

    .hero p {
        color: #786858;
        font-size: 14px;
        line-height: 1.9;
        max-width: 610px;
        margin-bottom: 0;
    }

    /* ===== Section headings ===== */
    .section-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 23px;
        font-weight: 700;
        color: var(--espresso);
        margin: 20px 0 7px;
    }

    .section-description {
        color: #887767;
        font-size: 13px;
        line-height: 1.7;
        margin-bottom: 17px;
    }

    /* ===== File uploader ===== */
    div[data-testid="stFileUploader"] {
        background: #fffdf8;
        border: 1px dashed #bda579;
        border-radius: 14px;
        padding: 17px;
        box-shadow: 0 5px 18px #39291f08;
    }

    div[data-testid="stFileUploader"] section {
        background: transparent;
    }

    div[data-testid="stFileUploader"] small {
        color: #8b7968;
    }

    div[data-testid="stFileUploader"] button {
        background: #efe4d2;
        color: #59402f;
        border: 1px solid #ddc8a8;
        border-radius: 8px;
        font-weight: 600;
    }

    div[data-testid="stFileUploader"] button:hover {
        background: #e5d3b8;
        color: #39291f;
        border-color: #aa854b;
    }

    /* ===== Text area ===== */
    div[data-testid="stTextArea"] textarea {
        background: #fffdf8 !important;
        color: #39291f !important;
        border: 1px solid #ddcfbc !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        line-height: 1.8 !important;
        box-shadow: inset 0 1px 3px #39291f05;
        transition: border-color 0.2s ease,
                    box-shadow 0.2s ease;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #aa854b !important;
        box-shadow: 0 0 0 2px #aa854b20 !important;
    }

    div[data-testid="stTextArea"] textarea::placeholder {
        color: #aa9a88 !important;
    }

    /* ===== Slider ===== */
    div[data-testid="stSlider"] [data-baseweb="slider"] {
        padding-top: 8px;
    }

    div[data-testid="stSlider"] [role="slider"] {
        background: #aa854b !important;
        border: 2px solid #fffdf8 !important;
        box-shadow: 0 0 0 1px #aa854b;
    }

    div[data-testid="stSlider"] [data-testid="stTickBar"] {
        background: #dfcfb8;
    }

    /* ===== Dropdowns ===== */
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #fffdf8;
        border-color: #ddcfbc;
        border-radius: 9px;
        color: #39291f;
    }

    div[data-testid="stSelectbox"] [data-baseweb="select"]:hover > div {
        border-color: #aa854b;
    }

    /* ===== Main action button ===== */
    div.stButton > button {
        width: 100%;
        min-height: 49px;
        border-radius: 9px;
        background: linear-gradient(
    115deg,
    #d9bd87,
    #f0dfbd
);
color: #39291f;
        color: #fffaf1;
        border: 1px solid #493326;
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.2px;
        box-shadow:
            0 5px 14px #39291f19,
            inset 0 1px 0 #ffffff12;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(
            115deg,
            #674b32,
            #80603d
        );
        color: #ffffff;
        border-color: #b08b51;
        box-shadow: 0 7px 20px #39291f22;
        transform: translateY(-1px);
    }

    div.stButton > button:focus:not(:active) {
        border-color: #c6a66c;
        color: #ffffff;
        box-shadow: 0 0 0 2px #aa854b35;
    }

    div.stButton > button:disabled {
        background: #d9cbb8;
        color: #95816c;
        border-color: #d9cbb8;
        box-shadow: none;
        transform: none;
    }

    /* ===== Download button ===== */
    div.stDownloadButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 9px;
        background: #f0e5d2;
        border: 1px solid #d9c29e;
        color: #59402f;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    div.stDownloadButton > button:hover {
        background: #e7d5b8;
        border-color: #aa854b;
        color: #39291f;
    }

    /* ===== File information card ===== */
    .tip-card {
        background: linear-gradient(
            110deg,
            #eee3d2,
            #f7efe3
        );
        border: 1px solid #dfcfb8;
        border-left: 3px solid #aa854b;
        border-radius: 5px 11px 11px 5px;
        padding: 15px 18px;
        color: #654b37;
        font-size: 13px;
        line-height: 1.8;
        margin-top: 15px;
    }

    /* ===== Summary card ===== */
    .result-card {
        position: relative;
        background: #fffdf8;
        border: 1px solid #e3d5c2;
        border-radius: 5px 16px 16px 16px;
        padding: 29px;
        margin-top: 15px;
        margin-bottom: 17px;
        box-shadow:
            0 10px 30px #39291f0c,
            inset 0 1px 0 #ffffff;
    }

    
    /* ===== Key Points Cards ===== */

    .key-point-card {
        display: flex;
        align-items: flex-start;
        gap: 15px;
        background: #fffdf8;
        border: 1px solid #e4d8c7;
        border-left: 3px solid #aa854b;
        border-radius: 5px 13px 13px 13px;
        padding: 18px 20px;
        margin: 12px 0;
        box-shadow: 0 5px 18px #39291f08;
        transition: all 0.2s ease;
    }

    .key-point-card:hover {
        border-color: #c6a66c;
        box-shadow: 0 8px 22px #39291f12;
        transform: translateY(-2px);
    }

    .key-point-number {
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 36px;
        height: 36px;
        background: #efe3ce;
        border: 1px solid #ddc9a6;
        border-radius: 9px;
        color: #785a35;
        font-family: 'Manrope', sans-serif;
        font-size: 13px;
        font-weight: 800;
    }

    .key-point-text {
        color: #59402f;
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        line-height: 1.9;
        padding-top: 5px;
        overflow-wrap: anywhere;
    }

    @media (prefers-reduced-motion: reduce) {
        .key-point-card {
            transition: none;
        }

        .key-point-card:hover {
            transform: none;
        }
    }


    .result-label {
        color: #98723c;
        font-family: 'Manrope', sans-serif;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .result-heading {
        color: #39291f;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 27px;
        font-weight: 700;
        line-height: 1.35;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .result-text {
        color: #5c4a3b;
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        line-height: 2;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }

    /* ===== Informational messages ===== */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* ===== Caption text ===== */
    div[data-testid="stCaptionContainer"] {
        color: #8b7968;
        font-size: 12px;
        line-height: 1.7;
    }

    /* ===== Footer ===== */
    .footer {
        border-top: 1px solid #dfd0bc;
        margin-top: 43px;
        padding-top: 21px;
        color: #978574;
        font-family: 'DM Sans', sans-serif;
        font-size: 11px;
        letter-spacing: 0.5px;
        line-height: 1.8;
        text-align: center;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer {
        visibility: hidden;
    }

    /* ===== Mobile responsive design ===== */
    @media (max-width: 640px) {
        .block-container {
            padding-top: 1.3rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .brand {
            margin-bottom: 18px;
        }

        .hero {
            padding: 28px 23px;
            margin-bottom: 25px;
        }

        .hero h1 {
            font-size: 33px;
        }

        .hero p {
            font-size: 13px;
        }

        .section-title {
            font-size: 21px;
        }

        .result-card {
            padding: 21px;
        }

        .result-heading {
            font-size: 23px;
        }

        .result-text {
            font-size: 13px;
            line-height: 1.9;
        }
    }

    /* ===== Reduced motion accessibility ===== */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            transition: none !important;
            transform: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 3. Header
# -------------------------------

st.markdown("""
<div class="brand">✳ CLARITY</div>

<div class="hero">
    <div class="hero-label">✦ YOUR PERSONAL STUDY ASSISTANT</div>
    <h1>Less reading.<br>More understanding.</h1>
    <p>
        Turn lengthy documents into concise, useful summaries.
        Upload your notes, research papers, or study material
        and find the key information faster.
    </p>
</div>
""", unsafe_allow_html=True)


# -------------------------------
# 4. Text extraction
# -------------------------------

def extract_text(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    elif filename.endswith(".docx"):
        document = Document(uploaded_file)
        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)

    elif filename.endswith(".txt"):
        return uploaded_file.getvalue().decode(
            "utf-8-sig",
            errors="replace"
        )

    return ""

# -------------------------------
# 5. Summarisation
# -------------------------------


def summarize_text(text, sentence_count):

    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    summarizer = LexRankSummarizer()

    sentences = summarizer(
        parser.document,
        sentence_count
    )

    selected_sentences = [
        str(sentence).strip()
        for sentence in sentences
    ]

    # Remove duplicate sentences
    unique_sentences = []
    seen = set()

    for sentence in selected_sentences:
        key = sentence.lower()

        if key not in seen:
            seen.add(key)
            unique_sentences.append(sentence)

    # Organise the summary into readable paragraphs
    summary = ""

    for i, sentence in enumerate(unique_sentences):
        summary += sentence + " "

        # Start a new paragraph after every 3 sentences
        if (i + 1) % 3 == 0:
            summary += "\n\n"

    return summary.strip()
# -------------------------------
# Key Points Extractor
# -------------------------------

def extract_key_points(text, number_of_points=5):
    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    summarizer = LexRankSummarizer()

    sentences = summarizer(
        parser.document,
        number_of_points
    )

    points = []

    for sentence in sentences:
        points.append(str(sentence))

    return points


# -------------------------------
# Mind Map Concept Extractor
# -------------------------------

nlp = spacy.load("en_core_web_sm")

def extract_concepts(text, max_concepts=12):

    keyword_extractor = yake.KeywordExtractor(
        lan="en",
        n=3,
        top=max_concepts * 3
    )

    keywords = keyword_extractor.extract_keywords(text)

    concepts = []
    seen = set()

    def add_concept(phrase):
        phrase = " ".join(phrase.split()).strip(" .,:;!?-")

        if len(phrase) < 3 or len(phrase.split()) > 5:
            return

        key = phrase.lower()

        if key not in seen:
            seen.add(key)
            concepts.append(phrase)

    # Add important phrases first
    for phrase, score in keywords:
        add_concept(phrase)

        if len(concepts) >= max_concepts:
            break

    # Add useful noun phrases if more concepts are needed
    if len(concepts) < max_concepts:
        doc = nlp(text[:100000])

        for chunk in doc.noun_chunks:
            add_concept(chunk.text)

            if len(concepts) >= max_concepts:
                break

    return concepts[:max_concepts]

# -------------------------------
# 8. Summary settings
# -------------------------------


# Upload your document
uploaded_file = st.file_uploader(
    "Drop your file here or browse",
    type=["pdf", "docx", "txt"]
)

# Paste your text
text_input = st.text_area(
    "Paste or type your text here",
    height=250,
    placeholder="Start typing or paste your text here..."
)


st.markdown(
    '<div class="section-title">02 &nbsp; Make it yours</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    summary_style = st.selectbox(
        "Choose summary style",
        ["Concise", "Balanced", "Detailed"]
    )

    sentence_count = st.slider(
        "Summary length (number of sentences)",
        min_value=5,
        max_value=200,
        value=30,
        step=5
    )

with right:
    number_of_points = st.slider(
        "Number of key points",
        min_value=3,
        max_value=15,
        value=5,
        step=1
    )

    st.markdown(
        '<div style="padding-top:9px;color:#858095;'
        'font-size:13px;">'
        
        '</div>',
        unsafe_allow_html=True
    )
# -------------------------------
# 9. Generate summary
# -------------------------------

st.write("")

# Use pasted text if provided; otherwise use the uploaded file
if text_input.strip():
    current_source = "text:" + text_input
elif uploaded_file is not None:
    current_source = "file:" + uploaded_file.name
else:
    current_source = None

if st.button(
    "✦  Generate my summary",
    type="primary",
    disabled=current_source is None
):
    try:
        # Get text from the selected input
        if text_input.strip():
            text = text_input
            output_filename = "pasted_text_summary.txt"
            source_name = "Pasted text"
        else:
            text = extract_text(uploaded_file)
            output_filename = (
                uploaded_file.name.rsplit(".", 1)[0]
                + "_summary.txt"
            )
            source_name = uploaded_file.name

        if not text.strip():
            st.warning(
                "No readable text was found. "
                "Scanned PDFs may require OCR."
            )

        else:
            max_characters = 100000

            if len(text) > max_characters:
                text = text[:max_characters]

                st.info(
                    "This text is long. Only the first "
                    "100,000 characters will be summarised."
                )

            with st.spinner(
                "Finding the most important sentences..."
            ):
                summary = summarize_text(
                    text,
                    sentence_count
                )

            if summary.strip():
                st.session_state["summary"] = summary
                st.session_state["source_text"] = text
                st.session_state["summary_filename"] = (
                    output_filename
                )
                st.session_state["summary_source"] = (
                    current_source
                )
            else:
                st.warning(
                    "Not enough readable text was found "
                    "to create a summary."
                )

    except Exception as error:
        st.error("Something went wrong while summarising.")
        st.caption(
            f"{type(error).__name__}: {error}"
        )
# -------------------------------
# 10. Results section
# -------------------------------

if (
    st.session_state.get("summary")
    and current_source is not None
    and st.session_state.get("summary_source")
    == current_source
):
    
    summary = st.session_state["summary"]

    # Save the original text used for the summary
    if "source_text" not in st.session_state:
        st.session_state["source_text"] = ""

    source_text = st.session_state["source_text"]

    # -------------------------------
    # Document Insights
    # -------------------------------

    original_words = len(source_text.split())
    summary_words = len(summary.split())

    parser = PlaintextParser.from_string(
        source_text,
        Tokenizer("english")
    )
    original_sentences = len(parser.document.sentences)

    reading_time = max(1, math.ceil(original_words / 200))

    if original_words > 0:
        compression = round(
            (1 - summary_words / original_words) * 100
        )
    else:
        compression = 0

    st.markdown(
        '<div class="section-title">Document Insights</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Original Words", f"{original_words:,}")
    col2.metric("Sentences", f"{original_sentences:,}")
    col3.metric("Reading Time", f"~{reading_time} min")
    col4.metric("Summary Words", f"{summary_words:,}")
    col5.metric("Compression", f"{compression}%")


    st.markdown(
        '<div class="section-title">03 &nbsp; Your summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">✦ SUMMARY READY</div>
            <div class="result-heading">The key ideas, simplified.</div>
            <div class="result-text">{summary}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.download_button(
        "↓  Download summary",
        data=summary,
        file_name=st.session_state["summary_filename"],
        mime="text/plain",
        use_container_width=True
    )

    st.caption(
        "Note: LexRank selects sentences from the original text. "
        "It does not rewrite or fact-check the document."
    ) 
    # -------------------------------
    # Key Points Display
    # -------------------------------

    st.markdown(
        '<div class="section-title">04 &nbsp; Key Points to Remember</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Your main takeaways, organised for quick revision.'
        '</div>',
        unsafe_allow_html=True
    )

    key_points = extract_key_points(
        source_text,
        number_of_points
    )

    if key_points:
        for i, point in enumerate(key_points, start=1):
            st.markdown(
                f"""
                <div class="key-point-card">
                    <div class="key-point-number">
                        {i:02d}
                    </div>
                    <div class="key-point-text">
                        {point}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No key points could be extracted.")
    
    
    
    # -------------------------------
    # 05. Visual Mind Map
    # -------------------------------

    st.markdown(
        '<div class="section-title">05 &nbsp; Visual Mind Map</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Explore important concepts and their explanations '
        'from your document.'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button("✦ Generate Mind Map"):

        concepts = extract_concepts(source_text, 12)

        parser = PlaintextParser.from_string(
            source_text,
            Tokenizer("english")
        )

        sentences = [
            str(s).strip()
            for s in parser.document.sentences
            if len(str(s).split()) >= 5
        ]

        if not concepts or not sentences:
            st.warning(
                "Not enough readable text was found to create "
                "a useful mind map."
            )

        else:

            stop_words = {
                "the", "and", "for", "with", "from", "that",
                "this", "are", "was", "were", "has", "have",
                "had", "into", "their", "they", "them", "its",
                "about", "which", "when", "where", "what",
                "how", "can", "may", "also", "such", "these",
                "those", "using", "used"
            }

            topics = []

            for concept in concepts:

                concept_words = {
                    word.lower().strip(".,:;!?()[]{}")
                    for word in concept.split()
                    if len(word) > 2
                    and word.lower() not in stop_words
                }

                best_sentence = ""
                best_score = 0

                # Find the sentence most closely related
                # to this concept
                for sentence in sentences:

                    sentence_words = {
                        word.lower().strip(".,:;!?()[]{}")
                        for word in sentence.split()
                    }

                    common_words = concept_words.intersection(
                        sentence_words
                    )

                    score = len(common_words)

                    # Give preference to sentences containing
                    # the complete concept phrase
                    if concept.lower() in sentence.lower():
                        score += 3

                    if score > best_score:
                        best_score = score
                        best_sentence = sentence

                # Shorten the explanation for the diagram
                explanation = best_sentence

                if len(explanation) > 150:
                    explanation = (
                        explanation[:147].rsplit(" ", 1)[0] + "..."
                    )

                if not explanation:
                    explanation = "See the original document for context."

                topics.append({
                    "title": concept,
                    "explanation": best_sentence
                })

            def dot_escape(value):
                return (
                    str(value)
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", " ")
                )

            colors = [
                "#F3E6CC",
                "#E6E5D8",
                "#E9DED0"
            ]

            dot = """
            digraph MindMap {
                graph [
                    rankdir=LR,
                    bgcolor="transparent",
                    pad=0.4,
                    nodesep=0.35,
                    ranksep=0.8,
                    splines=curved
                ];

                node [
                    shape=box,
                    style="rounded,filled",
                    fontname="Arial",
                    fontsize=10,
                    margin="0.18,0.12",
                    color="#D8C5A5",
                    fontcolor="#39291F"
                ];

                edge [
                    color="#B49A78",
                    penwidth=1.5,
                    arrowsize=0.6
                ];

                center [
                    label="DOCUMENT\\nOVERVIEW",
                    fillcolor="#DCC28F",
                    color="#A9854B",
                    penwidth=2,
                    fontsize=14
                ];
            """

            for i, topic in enumerate(topics):

                topic_id = f"concept{i}"
                detail_id = f"detail{i}"

                color = colors[i % len(colors)]

                explanation = topic["explanation"]

                if len(explanation) > 150:
                    explanation = (
                        explanation[:147].rsplit(" ", 1)[0] + "..."
                    )

                dot += f'''
                    {topic_id} [
                        label="{dot_escape(topic["title"])}",
                        fillcolor="{color}",
                        fontsize=11
                    ];

                    {detail_id} [
                        label="{dot_escape(explanation)}",
                        fillcolor="#FFFCF6",
                        fontsize=9
                    ];

                    center -> {topic_id};
                    {topic_id} -> {detail_id};
                '''

            dot += "}"

            st.session_state["mind_map_dot"] = dot
            st.session_state["mind_map_topics"] = topics
            st.session_state["mind_map_source"] = current_source

    # Show the generated map for the current document
    if (
        st.session_state.get("mind_map_dot")
        and st.session_state.get("mind_map_source") == current_source
    ):

        st.graphviz_chart(
            st.session_state["mind_map_dot"],
            use_container_width=True
        )

        st.download_button(
            "↓ Download Mind Map Source",
            data=st.session_state["mind_map_dot"],
            file_name="clarity_mind_map.dot",
            mime="text/vnd.graphviz",
            use_container_width=True
        )

        st.markdown(
            '<div class="section-title">Topic Explanations</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Read the supporting information for each concept.'
            '</div>',
            unsafe_allow_html=True
        )

        for i, topic in enumerate(
            st.session_state["mind_map_topics"],
            start=1
        ):

            with st.expander(
                f"{i:02d} · {topic['title']}"
            ):

                if topic["explanation"]:
                    st.write(topic["explanation"])
                else:
                    st.info(
                        "No matching sentence was found. "
                        "Please check the original document."
                    )

                st.caption(
                    "This explanation is taken from the source text."
                )

# -------------------------------
# 11. Footer
# -------------------------------
st.markdown("""
<div class="footer">
    CLARITY &nbsp; · &nbsp; Built with Python and Streamlit
    <br><br>
    Free to use · No paid API required
</div>
""", unsafe_allow_html=True)