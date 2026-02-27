import streamlit as st
from llm_engine import analyze_resume
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="AI Placement Intelligence System", page_icon="🚀", layout="centered")

# ----------
# -------------------- LOGIN SYSTEM --------------------



# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Resume Analyzer", "About System"])

# ---------------- ABOUT PAGE ---------------- #

if page == "About System":
    st.title("📘 About AI Placement Intelligence System")
    st.write("""
    This system evaluates placement readiness using a Local LLM (Ollama).
    
    Features:
    - Resume analysis
    - Skill gap detection
    - Placement readiness scoring
    - Interview question generation
    - 30-day improvement roadmap
    
    Designed for students preparing for placements.
    """)
    st.stop()

# ---------------- MAIN ANALYZER PAGE ---------------- #

st.title("🚀 AI Placement Readiness Intelligence System")
st.write("Upload your resume or paste text to evaluate placement readiness using AI.")

st.markdown("### 🤖 AI Engine Status")
st.info("Using Local LLM (Ollama)")

resume_text = ""

# Upload PDF
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text()

# Manual Paste
st.markdown("### OR")
manual_text = st.text_area("✍ Paste Resume Text Here")

if manual_text:
    resume_text = manual_text

# Resume Preview
if resume_text:
    st.markdown("### 📄 Resume Preview")
    st.text(resume_text[:500] + "...")

# Company Type
company_type = st.selectbox(
    "🏢 Select Target Company Type",
    [
        "Product-based (High DSA focus)",
        "Service-based (Core fundamentals focus)",
        "Startup (Full-stack + adaptability focus)"
    ]
)

# Analyze Button
if st.button("🔍 Analyze Resume"):

    if resume_text:

        with st.spinner("AI is analyzing your resume... Please wait."):
            result = analyze_resume(resume_text, company_type)

        st.success("Analysis Complete!")

        # ---------------- SCORE EXTRACTION ---------------- #

        score_match = re.search(r"(\d+)/10", result)
        if score_match:
            score = int(score_match.group(1))
            st.metric("🏆 Placement Readiness Score", f"{score}/10")
            st.progress(score / 10)

        st.divider()

        # Detailed Result
        with st.expander("📊 View Detailed AI Analysis", expanded=True):
            st.markdown(result)

        # Download Button
        st.download_button(
            label="📥 Download Report",
            data=result,
            file_name="placement_analysis.txt",
            mime="text/plain"
        )

    else:
        st.warning("Please upload or paste resume before analyzing.")

st.divider()
st.caption("Built using Local LLM (Ollama) + Streamlit | Hackathon Project 2026")