from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

# ✅ Allow requests from your frontend / Django app
origins = [
    "*",  # You can replace "*" later with your exact frontend URLs
    "https://skillmatch-frontend.onrender.com",
    "https://skillmatch-django.onrender.com",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Load the model once globally
model = SentenceTransformer("all-MiniLM-L6-v2")

class ResumeRequest(BaseModel):
    resume_text: str
    jobs: list  # Each job: dict with id, title, description, url

@app.post("/recommend")
def recommend(data: ResumeRequest):
    resume_emb = model.encode(data.resume_text, convert_to_tensor=True)
    results = []
    for job in data.jobs:
        job_emb = model.encode(job["description"], convert_to_tensor=True)
        score = float(util.cos_sim(resume_emb, job_emb))
        results.append({
            "id": job["id"],
            "title": job["title"],
            "description": job["description"],
            "url": job["url"],
            "score": score
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)[:10]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001)
