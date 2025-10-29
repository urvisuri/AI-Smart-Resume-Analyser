import re
from pdfminer.high_level import extract_text

def parse_resume(file_path):
    text = extract_text(file_path)

    # Name (assumed first non-empty line)
    lines = text.strip().split('\n')
    name = lines[0] if lines else ""

    # Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else ""

    # Skills - look for common skill keywords
    skill_keywords = [
        'Python', 'Java', 'C++', 'HTML', 'CSS', 'JavaScript', 'SQL', 'Git', 'Excel',
        'AI', 'Machine Learning', 'Communication', 'Agile', 'AWS', 'GCP', 'Azure',
        'UI', 'UX', 'Design', 'Engineering', 'Teamwork'
    ]
    found_skills = [skill for skill in skill_keywords if skill.lower() in text.lower()]

    # Experience section
    experience_section = []
    if "experience" in text.lower():
        exp_lines = [line for line in lines if "experience" in line.lower()]
        experience_section.extend(exp_lines)

    return {
        "name": name,
        "email": email,
        "skills": list(set(found_skills)),  # Remove duplicates
        "experience": experience_section if experience_section else ["Not specified"]
    }
