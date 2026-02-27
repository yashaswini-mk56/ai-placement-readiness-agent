import streamlit as st
from llm_engine import analyze_resume
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Placement Agent", layout="centered")

st.title("🚀 AI Placement Readiness Agent")
st.write("Upload your resume (PDF) or paste text to evaluate placement readiness.")

# --- Upload PDF ---
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

resume_text = ""

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text()

# --- OR Manual Paste ---
st.markdown("### OR")
manual_text = st.text_area("Paste Resume Text Here")

if manual_text:
    resume_text = manual_text

# --- Company Type ---
company_type = st.selectbox(
    "Select Target Company Type",
    ["Product-based", "Service-based", "Startup"]
)

# --- Analyze ---
if st.button("Analyze Resume"):
    if resume_text:
        with st.spinner("Analyzing with AI..."):
            result = analyze_resume(resume_text, company_type)

        st.success("Analysis Complete!")
        st.markdown("### 📊 AI Evaluation Result")
        st.markdown(result)

    else:
        st.warning("Please upload or paste resume.")