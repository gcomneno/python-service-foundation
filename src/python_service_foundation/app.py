from fastapi import FastAPI

app = FastAPI(
    title="Python Service Foundation",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "python-service-foundation"}
