import os
import requests
from PyPDF2 import PdfReader
import docx
import requests
from .models import Job

def parse_resume(file_path):
    text = ""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif ext in [".docx", ".doc"]:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def get_recommendations_from_fastapi(resume_text, jobs):
    ENV=os.environ.get("ENV","local").lower()
    if ENV=="local":
         url = "http://127.0.0.1:8001/recommend"
    else:
        url = "https://skillmatch-fastapi.onrender.com/recommend"    
    
  # ← replace once confirmed
    payload = {
        "resume_text": resume_text,
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "url": getattr(job, "url", "#"),
            }
            for job in jobs
        ],
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("⚠️ FastAPI request failed:", e)
        return []
def fetch_jobs_from_remoteok(limit=100):
    urls = [
        "https://remoteok.com/api",  # direct
        "https://api.allorigins.win/raw?url=https://remoteok.com/api",
        "https://r.jina.ai/https://remoteok.com/api",  # very reliable
    ]

    data = None
    for url in urls:
        try:
            print(f"🌐 Trying {url}")
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(f"✅ Success: fetched from {url}")
            break
        except Exception as e:
            print(f"❌ Failed: {url} — {e}")

    if not data:
        print("🚨 All RemoteOK sources failed")
        return []

    jobs = []
    for job in data[1:limit+1]:
        title = job.get("position", "No Title")
        desc = job.get("description", "")[:300]
        job_link = job.get("url") or None

        job_obj = Job.objects.create(
            title=title,
            description=desc,
            link=job_link,
        )

        jobs.append({
            "id": job_obj.id,
            "title": title,
            "description": desc,
            "link": job_link,
        })

    return jobs
