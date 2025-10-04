import re

def calculate_ats_score(resume_text, job_description):
    """
    Simple ATS score based on keyword overlap.
    Returns a score (0–100).
    """
    if not resume_text or not job_description:
        return 0
    
    # Lowercase & tokenize
    resume_words = set(re.findall(r"\w+", resume_text.lower()))
    job_words = set(re.findall(r"\w+", job_description.lower()))

    # Calculate overlap
    common_words = resume_words.intersection(job_words)
    
    if not job_words:
        return 0
    
    score = (len(common_words) / len(job_words)) * 100
    return round(score, 2)
