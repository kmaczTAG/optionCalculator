# ---------- Builder stage ----------
    FROM python:3.12-slim AS builder
    WORKDIR /app
    
    # Install deps
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ---------- Runtime stage ----------
    FROM python:3.12-slim
    WORKDIR /app
    
    # Pull the packages we just built
    COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
    
    # Copy the *actual* source code (the folder that really exists)
    COPY app ./
    
    EXPOSE 8000
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]