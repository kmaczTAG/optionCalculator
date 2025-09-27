from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import HelloRequest

app = FastAPI(title="Option‑Tool API")

# --------------------------------------------------------------
# CORS – allow the React dev server (http://localhost:5173) to call us
# --------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # In prod replace with your actual origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check() -> dict:
    """Simple health endpoint used by the front‑end."""
    return {"status": "ok"}

@app.post("/api/hello")
def say_hello(payload: HelloRequest) -> dict:
    """
    Echoes back a greeting.
    Example request body: {"name":"Alice"}
    """
    return {"greeting": f"Hello, {payload.name}!"}