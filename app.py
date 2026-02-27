import streamlit as st
from llm_engine import analyze_resume
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="AI Placement Intelligence System", page_icon="🚀", layout="centered")

# --------------

# ---------------- PREMIUM UI LOGIN SYSTEM ---------------- #

# Global Styling (Before Login)
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Center content properly */
.block-container {
    padding-top: 4rem;
    max-width: 600px;
}

/* Login Card */
.login-card {
    background-color: #1e293b;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.4);
}

/* Title */
.login-title {
    color: #ffffff;
    text-align: center;
    font-size: 30px;
    font-weight: 700;
}

/* Subtitle */
.login-subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

/* Input field background + text color */
.stTextInput>div>div>input {
    background-color: #334155 !important;
    color: #ffffff !important;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #475569;
}

/* Placeholder text color */
.stTextInput input::placeholder {
    color: #94a3b8 !important;
}

/* Button styling */
.stButton>button {
    background-color: #6366f1;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #4f46e5;
}

/* Remove footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown('<div class="login-title">🚀 AI Placement Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Smart Resume Evaluation Platform</div>', unsafe_allow_html=True)

        email = st.text_input("📧 Email Address")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):

            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            email_valid = re.match(email_pattern, email)

            if not email_valid:
                st.error("❌ Please enter a valid email address.")

            elif len(password) < 8:
                st.error("❌ Password must be at least 8 characters.")

            elif not any(char.isdigit() for char in password):
                st.error("❌ Password must contain at least one number.")

            else:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Login successful!")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

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