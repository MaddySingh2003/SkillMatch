from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")  # ~300 MB


class ResumeRequest(BaseModel):
    resume_text: str
    jobs: list  # Each job: dict with id, title, description, url



@app.post("/recommend")
def recommend(data: ResumeRequest):
    resume_text = data.resume_text
    jobs = data.jobs
    


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

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:10]



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001)

