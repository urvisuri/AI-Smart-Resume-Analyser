import streamlit as st
from utils.resume_parser import parse_resume
from database.db import insert_data, create_table
from utils.score_calculator import calculate_score  # Import at the beginning

# Setup
st.set_page_config(page_title="AI Smart Resume Analyser", layout="centered")
st.markdown(
    "<style>" + open("assets/custom.css").read() + "</style>",
    unsafe_allow_html=True
)
create_table()

# Title & Sidebar
st.title("📄 AI Smart Resume Analyser")
st.markdown("Developed with ❤️ by **Urvi Suri**")

st.sidebar.image("assets/logo.png", width=200)
st.sidebar.markdown("Upload a resume below:")

# File Upload
uploaded_file = st.file_uploader("Choose a resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    with open(f"data/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded successfully!")

    result = parse_resume(f"data/{uploaded_file.name}")

    st.subheader("🔍 Extracted Resume Data (Editable)")

    # Editable form inputs
    name = st.text_input("👤 Name", result.get("name", ""))
    email = st.text_input("📧 Email", result.get("email", ""))
    skills = st.text_area("🛠️ Skills (comma-separated)", ", ".join(result.get("skills", [])))
    experience = st.text_area("💼 Experience", "\n".join(result.get("experience", [])))

    if st.button("💾 Save Modified Data"):
        updated_result = {
            "name": name,
            "email": email,
            "skills": [s.strip() for s in skills.split(",") if s.strip()],
            "experience": [e.strip() for e in experience.split("\n") if e.strip()]
        }

        st.success("✅ Modified Resume Data Saved!")
        st.json(updated_result)

        # Save to database
        insert_data(updated_result)

        # Skill Suggestions
        st.subheader("💡 Resume Suggestions")
        skills_lower = [skill.lower() for skill in updated_result["skills"]]
        missing_skills = []

        if "sql" not in skills_lower:
            missing_skills.append("SQL")
        if not any(cloud in skills_lower for cloud in ["aws", "gcp", "azure"]):
            missing_skills.append("Cloud platforms (AWS/GCP/Azure)")
        if "git" not in " ".join(skills_lower):
            missing_skills.append("Version control (Git/GitHub)")

        if missing_skills:
            st.markdown(f"**Consider learning:** {', '.join(missing_skills)} to strengthen your technical profile.")

        # Role Suggestions
        if "ux" in skills_lower or "ui" in skills_lower:
            st.markdown("🎯 You might be a good fit for **UI/UX Designer** or **Product Designer** roles.")
        elif "python" in skills_lower and "ai" in skills_lower:
            st.markdown("🎯 Explore roles like **Machine Learning Engineer** or **Data Scientist**.")

        # Experience Suggestions
        exp_text = " ".join(updated_result["experience"])
        if len(exp_text.strip()) < 20:
            st.markdown("📝 Add more details in your experience section — like internships, college projects, or volunteering.")

        # Smart Resume Enhancements
        st.subheader("🔧 Smart Resume Enhancements")

        # 1. Project Suggestions
        if "python" in skills_lower and "ai" in skills_lower:
            st.markdown("- 💡 Consider adding a project like: **AI Chatbot**, **Resume Parser**, or **Sentiment Analyzer**.")
        if "web" in " ".join(skills_lower) or "html" in skills_lower:
            st.markdown("- 💡 Add a project like: **Portfolio Website**, **E-commerce Store**, or **Blog CMS**.")

        # 2. Certification Suggestions
        cert_suggestions = []
        if "cloud" not in " ".join(skills_lower):
            cert_suggestions.append("AWS Certified Cloud Practitioner")
        if "data" not in skills_lower:
            cert_suggestions.append("Google Data Analytics Certificate")
        if "git" not in " ".join(skills_lower):
            cert_suggestions.append("Version Control with Git (Coursera)")

        if cert_suggestions:
            st.markdown("📜 **Recommended Certifications:**")
            for cert in cert_suggestions:
                st.markdown(f"- {cert}")

        # 3. Profile/Link Suggestions
        st.markdown("🌐 **Make sure your resume includes:**")
        st.markdown("- 🔗 GitHub profile link")
        st.markdown("- 🔗 LinkedIn profile link")
        st.markdown("- 📱 Phone number")

        # 4. Section Suggestions
        if len(updated_result["experience"]) < 2:
            st.markdown("🧠 Add more detailed experience: internships, projects, research papers, or open-source contributions.")

        # Calculate and Display Resume Score
        resume_score = calculate_score(updated_result)  # Calculate the score using the updated resume data
        st.subheader("🏆 Resume Score")
        st.write(f"Your resume score is: {resume_score}/100")
