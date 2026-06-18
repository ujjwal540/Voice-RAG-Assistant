FROM python:3.12-slim

WORKDIR /app

ARG DATABASE_URL
ARG GROQ_API_KEY
ARG GOOGLE_API_KEY
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  DATABASE_URL=${DATABASE_URL} \
  GROQ_API_KEY=${GROQ_API_KEY} \
  GOOGLE_API_KEY=${GOOGLE_API_KEY}

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
