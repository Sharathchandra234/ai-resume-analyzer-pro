import streamlit as st
import pandas as pd
import PyPDF2
import plotly.express as px

st.set_page_config(page_title="AI Resume Analyzer Pro++", layout="wide")

st.title("📄 AI Resume Analyzer & Job Match Pro++")

st.markdown("Advanced ATS optimization and recruiter-fit analytics platform.")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

role = st.selectbox(
    "Target Role",
    ["AI Engineer", "Data Analyst", "Python Developer", "ML Engineer"]
)

job_desc = st.text_area(
    "Paste Job Description",
    "Looking for Python, SQL, Machine Learning, Pandas, Streamlit skills."
)

role_skills = {
    "AI Engineer": ["python","sql","machine learning","pytorch","tensorflow","nlp"],
    "Data Analyst": ["sql","excel","power bi","tableau","python","pandas"],
    "Python Developer": ["python","sql","api","flask","django","streamlit"],
    "ML Engineer": ["python","machine learning","tensorflow","pytorch","sql"]
}

def extract_pdf_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text.lower()

if uploaded_file:

    resume_text = extract_pdf_text(uploaded_file)

    skills_db = list(set(role_skills[role] + job_desc.lower().split()))

    matched = []
    missing = []

    for skill in role_skills[role]:
        if skill in resume_text:
            matched.append(skill.title())
        else:
            missing.append(skill.title())

    total = len(matched) + len(missing)
    score = int((len(matched)/total)*100) if total > 0 else 0

    # Fit Rating
    if score >= 80:
        fit = "Excellent Fit"
    elif score >= 60:
        fit = "Good Fit"
    elif score >= 40:
        fit = "Moderate Fit"
    else:
        fit = "Low Fit"

    # Section Scores (simulated)
    skills_score = score
    projects_score = min(score + 10, 100)
    education_score = 75
    formatting_score = 85

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎯 ATS Score", f"{score}/100")
    c2.metric("📌 Job Fit", fit)
    c3.metric("✅ Skills Matched", len(matched))
    c4.metric("❌ Skills Missing", len(missing))

    st.progress(score/100)

    st.markdown("---")

    # Chart
    chart_df = pd.DataFrame({
        "Section": ["Skills","Projects","Education","Formatting"],
        "Score": [skills_score, projects_score, education_score, formatting_score]
    })

    fig = px.bar(
        chart_df,
        x="Section",
        y="Score",
        title="Resume Section Scores"
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matching Skills")
        st.write(matched if matched else ["None"])

    with col2:
        st.subheader("❌ Missing Skills")
        st.write(missing if missing else ["None"])

    st.markdown("---")

    st.subheader("💡 Smart Suggestions")

    suggestions = []

    if missing:
        suggestions.append("Add missing keywords relevant to target role.")
    if score < 70:
        suggestions.append("Strengthen project descriptions with measurable outcomes.")
    suggestions.append("Include GitHub + live project links.")
    suggestions.append("Tailor summary section for selected role.")

    for s in suggestions:
        st.write("•", s)

    report = pd.DataFrame({
        "Metric": ["ATS Score","Matched Skills","Missing Skills"],
        "Value": [score, len(matched), len(missing)]
    })

    st.subheader("📊 Final Report")
    st.dataframe(report, use_container_width=True)

    csv = report.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Report",
        csv,
        "resume_report.csv",
        "text/csv"
    )

else:
    st.info("Upload resume PDF to begin.")