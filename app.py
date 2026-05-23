import streamlit as st
from pdf_parser import pdf_extract
from llm_engine import analyze_resume_general, analyze_role_match

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Resume Intelligence", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CACHED ANALYSIS FUNCTIONS
@st.cache_data
def run_general_analysis(text):
    return analyze_resume_general(text)

@st.cache_data
def run_role_match(text, role):
    return analyze_role_match(text, role)

# 3. HERO SECTION
st.markdown("<h1 style='text-align: center; color: #00C8FF;'>🚀 AI Resume Intelligence System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Upload your resume and get AI-powered career insights instantly</p>", unsafe_allow_html=True)
st.divider()

# 4. FILE UPLOADER (Fixed empty label issue)
uploaded_file = st.file_uploader("Please choose your Resume PDF file", type=["pdf"])

# 5. MAIN APPLICATION LOGIC (Scoped safely inside file checking)
if uploaded_file:
    st.success("✅ Resume uploaded successfully!")
    
    resume_text = pdf_extract(uploaded_file)
    
    if not resume_text:
        st.error("❌ Could not extract text from PDF")
        st.stop()
        
    with st.spinner("🔍 Analyzing Resume..."):
        data = run_general_analysis(resume_text)
        
    st.divider()
    
    # METRICS DISPLAY
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("🎯 Resume Score", f"{data.get('resume_score', 0)}%")
    m_col2.metric("📊 ATS Score", f"{data.get('ats_score', 0)}%")
    m_col3.metric("💼 Best Role", data.get('best_role', 'N/A'))
    
    st.progress(int(data.get('resume_score', 0)) / 100)
    st.divider()
    
    # NAVIGATION TABS
    tab1, tab2, tab3 = st.tabs(["📝 Analysis", "🎯 Role Match", "💡 Insights"])
    
    # ================= TAB 1: GENERAL ANALYSIS =================
    with tab1:
        t1_col1, t1_col2 = st.columns(2)
        
        with t1_col1:
            st.subheader("💡 Skills")
            skills_list = data.get("skills", [])
            if skills_list:
                # Cleaner styling for tags
                tags_html = "".join([f"<span style='background-color:#1E1E2F; color:#00C8FF; padding:6px 12px; margin:4px; border-radius:15px; display:inline-block;'>{skill}</span>" for skill in skills_list])
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.info("No skills detected.")
                
            st.subheader("⏳ Experience")
            st.info(data.get('experience', 'No experience details available.'))
            
        with t1_col2:
            st.subheader("🟢 Strengths")
            for strength in data.get("strengths", []):
                st.success(strength)
                
            st.subheader("🔴 Weaknesses")
            for weakness in data.get("weaknesses", []):
                st.error(weakness)
                
        st.subheader("📋 Suggestions")
        for sug in data.get("suggestions", []):
            st.warning(sug)
            
    # ================= TAB 2: ROLE MATCHING =================
    with tab2:
        roles = ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "Software Engineer"]
        selected_role = st.selectbox("🎯 Select Role to Compare Against", roles)
        custom_role = st.text_input("Or type a custom role title")
        
        final_role = custom_role if custom_role else selected_role
        
        if st.button("🔍 Run Compatibility Analysis"):
            with st.spinner(f"Matching resume with {final_role}..."):
                match_data = run_role_match(resume_text, final_role)
                
            st.metric("Match Score", f"{match_data.get('match_percentage', 0)}%")
            st.progress(int(match_data.get('match_percentage', 0)) / 100)
            
            t2_col1, t2_col2 = st.columns(2)
            with t2_col1:
                st.subheader("✅ Matching Skills")
                for skill in match_data.get("matching_skills", []):
                    st.success(skill)
            with t2_col2:
                st.subheader("❌ Missing Skills")
                for skill in match_data.get("missing_skills", []):
                    st.error(skill)
                    
            st.subheader("💡 Matching Rationale")
            st.info(match_data.get("reason", "No rationale provided."))
            
            st.subheader("📈 Recommended Improvements")
            for imp in match_data.get("improvement_suggestions", []):
                st.warning(imp)
                
    # ================= TAB 3: INSIGHTS (Now completely safe from crashing) =================
    with tab3:
        st.subheader("📊 Quick Insights")
        total_skills = len(data.get('skills', []))
        st.info(f"Total Unique Skills Detected: **{total_skills}**")
        
        score = data.get("resume_score", 0)
        if score > 75:
            # st.balloons()
            st.success("🔥 Strong Resume Profile! Your resume meets premium industrial standards.")
        elif score > 50:
            st.warning("⚠️ Average Resume Profile. Consider resolving the listed weaknesses to upgrade your score.")
        else:
            st.error("🚨 Needs Structural Improvement. Review the suggestions panel immediately.")
else:
    # App state before user drops a file
    st.info("👋 Welcome! Please upload a PDF resume above to run the AI engine.")
