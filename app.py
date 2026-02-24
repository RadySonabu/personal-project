from fastapi import FastAPI

app = FastAPI(title="FastAPI on Vercel")


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel"}


@app.get("/api/health")
async def health():
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
