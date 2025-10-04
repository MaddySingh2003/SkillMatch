from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

class ResumeRequest(BaseModel):
    resume_text: str
    jobs: list  # [{"id":1, "title":"Job", "description":"Desc"}]
@app.post("/recommend")
def recommend(data: dict):
    resume_text = data["resume_text"]
    jobs = data["jobs"]

    model = SentenceTransformer("all-MiniLM-L6-v2")

    resume_emb = model.encode(resume_text, convert_to_tensor=True)

    results = []
    for job in jobs:
        job_emb = model.encode(job["description"], convert_to_tensor=True)
        score = float(util.cos_sim(resume_emb, job_emb))
        results.append({
            "id": job["id"],
            "title": job["title"],
            "description": job["description"],
            "url": job["url"],
            "score": score
        })

    # ✅ sort by score (best matches first)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # ✅ return top 10 jobs only
    return results[:10]
