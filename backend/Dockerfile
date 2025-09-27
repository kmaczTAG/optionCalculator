# ---- Build stage -------------------------------------------------
    FROM python:3.12-slim AS builder
    WORKDIR /app
    
    # Copy only the requirements first (helps caching)
    COPY backend/requirements.txt .
    
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ---- Runtime stage -----------------------------------------------
    FROM python:3.12-slim
    WORKDIR /app
    
    # Bring the installed packages from the builder stage
    COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
    
    # Copy the *actual* source code (the folder that really exists)
    COPY backend/app ./app
    
    EXPOSE 8000
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]