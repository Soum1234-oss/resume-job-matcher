import re


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text, skill_list):
    text = clean_text(text)

    found = []

    for skill in skill_list:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found.append(skill)

    return sorted(set(found))