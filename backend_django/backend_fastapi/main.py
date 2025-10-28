from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()
model = None  # model will be loaded lazily

class ResumeRequest(BaseModel):
    resume_text: str
    jobs: list

@app.on_event("startup")
async def load_model():
    global model
    model = SentenceTransformer("all-MiniLM-L6-v2")

@app.post("/recommend")
def recommend(data: ResumeRequest):
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")  # fallback
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
