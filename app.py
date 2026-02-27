import streamlit as st
import re
from llm_engine import analyze_resume
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Placement Intelligence", layout="centered")

# -------------------- STYLING --------------------

st.markdown("""
<style>


h1, h2, h3 {
    color: white;
}

.stButton>button {
    background-color: #00c6ff;
    color: black;
    border-radius: 8px;
    height: 3em;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #0072ff;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -------------------- LOGIN SYSTEM --------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if not st.session_state.logged_in:
    st.title("🔐 Secure Login")

    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

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

    st.stop()

# -------------------- MAIN APP --------------------

st.sidebar.success(f"Logged in as: {st.session_state.user_email}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.rerun()

st.markdown("""
# 🚀 AI Placement Intelligence System
### 🎓 Smart Career Assistant Powered by Local LLM
""")

st.divider()

# -------------------- RESUME INPUT --------------------

st.subheader("📄 Resume Input")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

resume_text = ""

if uploaded_file:
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

else:
    resume_text = st.text_area("Or Paste Resume Text")

company_type = st.selectbox(
    "🎯 Select Target Company Type",
    ["Product-based", "Service-based", "Startup"]
)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    analyze_clicked = st.button("🚀 Analyze Resume", use_container_width=True)

# -------------------- ANALYSIS --------------------

if analyze_clicked:
    if resume_text:

        with st.spinner("🤖 AI is analyzing your resume..."):
            result = analyze_resume(resume_text, company_type)

        sections = result.split("\n\n")

        score = ""
        strengths = ""
        weaknesses = ""
        missing = ""
        questions = ""
        roadmap = ""

        for section in sections:
            if "SCORE" in section:
                score = section
            elif "STRENGTHS" in section:
                strengths = section
            elif "WEAKNESSES" in section:
                weaknesses = section
            elif "MISSING_SKILLS" in section:
                missing = section
            elif "INTERVIEW_QUESTIONS" in section:
                questions = section
            elif "ROADMAP" in section:
                roadmap = section

        st.divider()

        # Score Display
        st.subheader("📊 Placement Readiness Score")

        match = re.search(r"\d+", score)
        if match:
            numeric_score = int(match.group())
            st.metric("Score", f"{numeric_score}/10")
            st.progress(numeric_score / 10)
        else:
            st.info(score)

        # Strengths
        st.subheader("💪 Strengths")
        st.success(strengths)

        # Weaknesses
        st.subheader("⚠ Weaknesses")
        st.warning(weaknesses)

        # Missing Skills
        st.subheader("🧠 Missing Skills")
        st.error(missing)

        # Interview Questions
        st.subheader("❓ Interview Questions")
        st.write(questions)

        # Roadmap
        st.subheader("🗺 30-Day Roadmap")
        st.write(roadmap)

    else:
        st.warning("Please upload or paste resume.")

st.divider()

