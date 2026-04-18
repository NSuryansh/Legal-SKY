from fastapi import FastAPI

app = FastAPI(
    title="Legal-SKY Test",
    description="Minimal test app",
    version="1.0"
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Legal-SKY minimal test working"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "legal-sky-test"}
