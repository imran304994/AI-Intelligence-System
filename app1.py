import streamlit as st
from pdf_parser import pdf_extract
from llm_engine import analyze_resume_general, analyze_role_match

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Resume Intelligence", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #00C8FF;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
}

.skill-tag {
    background-color:#1E1E2F;
    padding:8px 12px;
    margin:5px;
    border-radius:20px;
    display:inline-block;
    color:#00C8FF;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO SECTION ----------
st.markdown("""
<h1 style='text-align: center;'>🚀 AI Resume Intelligence System</h1>
<p style='text-align: center; color:gray;'>
Upload your resume and get AI-powered career insights instantly
</p>
""", unsafe_allow_html=True)

# ---------- FILE UPLOAD ----------
st.markdown("### 📄 Upload Resume")
uploaded_file = st.file_uploader("", type=["pdf"])

@st.cache_data
def run_general_analysis(text):
    return analyze_resume_general(text)

# ---------- MAIN ----------
if uploaded_file:

    st.success("✅ Resume uploaded successfully!")

    resume_text = pdf_extract(uploaded_file)

    if not resume_text:
        st.error("❌ Could not extract text from PDF")
        st.stop()

    with st.spinner("🔍 Analyzing Resume..."):
        data = run_general_analysis(resume_text)

    st.divider()

    # ---------- METRICS ----------
    col1, col2, col3 = st.columns(3)

    col1.metric("🎯 Resume Score", f"{data['resume_score']}%")
    col2.metric("📊 ATS Score", f"{data['ats_score']}%")
    col3.metric("💼 Best Role", data["best_role"])

    st.progress(data["resume_score"] / 100)

    st.divider()

    # ---------- TABS ----------
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🎯 Role Match", "📈 Insights"])

    # ---------- TAB 1 ----------
    with tab1:

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("💡 Skills")

            skills_html = ""
            for skill in data["skills"]:
                skills_html += f"<span class='skill-tag'>{skill}</span>"

            st.markdown(skills_html, unsafe_allow_html=True)

            st.subheader("📈 Experience")
            st.markdown(f"<div class='card'>{data['experience']}</div>", unsafe_allow_html=True)

        with col2:
            st.subheader("🔥 Strengths")
            for s in data["strengths"]:
                st.markdown(f"<div class='card'>🔥 {s}</div>", unsafe_allow_html=True)

            st.subheader("⚠️ Weaknesses")
            for w in data["weaknesses"]:
                st.markdown(f"<div class='card'>⚠️ {w}</div>", unsafe_allow_html=True)

        st.subheader("🚀 Suggestions")
        for sug in data["suggestions"]:
            st.markdown(f"<div class='card'>💡 {sug}</div>", unsafe_allow_html=True)

    # ---------- TAB 2 ----------
    with tab2:

        roles = [
            "Data Scientist",
            "Data Analyst",
            "Machine Learning Engineer",
            "Software Engineer"
        ]

        selected_role = st.selectbox("🎯 Select Role", roles)
        custom_role = st.text_input("Or type custom role")

        final_role = custom_role if custom_role else selected_role

        if st.button("🚀 Analyze Match"):

            with st.spinner("🤖 Matching Resume..."):
                match_data = analyze_role_match(resume_text, final_role)

            st.metric("📊 Match Score", f"{match_data['match_percentage']}%")
            st.progress(match_data["match_percentage"] / 100)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matching Skills")
                for skill in match_data["matching_skills"]:
                    st.markdown(f"<div class='card'>✅ {skill}</div>", unsafe_allow_html=True)

            with col2:
                st.subheader("❌ Missing Skills")
                for skill in match_data["missing_skills"]:
                    st.markdown(f"<div class='card'>❌ {skill}</div>", unsafe_allow_html=True)

            st.subheader("🧠 Reason")
            st.info(match_data["reason"])

            st.subheader("🚀 Improvements")
            for imp in match_data["improvement_suggestions"]:
                st.markdown(f"<div class='card'>💡 {imp}</div>", unsafe_allow_html=True)

    # ---------- TAB 3 ----------
    with tab3:

        st.subheader("📈 Quick Insights")

        st.markdown(f"<div class='card'>Total Skills Detected: {len(data['skills'])}</div>", unsafe_allow_html=True)

        if data["resume_score"] > 75:
            st.success("Strong Resume 💪")
        elif data["resume_score"] > 50:
            st.warning("Average Resume ⚠️")
        else:
            st.error("Needs Improvement ❌")