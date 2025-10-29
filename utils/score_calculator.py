def calculate_score(data):
    score = 0

    # 1. Skills match
    core_skills = {"python", "sql", "git", "html", "css", "cloud", "ai"}
    resume_skills = {skill.lower() for skill in data.get("skills", [])}
    skill_score = len(core_skills.intersection(resume_skills)) / len(core_skills) * 30
    score += skill_score

    # 2. Experience
    exp = data.get("experience", [])
    if len(" ".join(exp)) > 100:
        score += 20
    elif len(exp) > 0:
        score += 10

    # 3. Projects
    if any("project" in e.lower() for e in exp):
        score += 15

    # 4. Contact completeness
    if data.get("email") and data.get("name"):
        score += 10

    # 5. Social profiles
    text_blob = " ".join(exp)
    if "linkedin" in text_blob.lower():
        score += 5
    if "github" in text_blob.lower():
        score += 5

    # 6. Certifications
    cert_keywords = ["certified", "course", "certification"]
    if any(keyword in text_blob.lower() for keyword in cert_keywords):
        score += 10

    return round(score, 2)
