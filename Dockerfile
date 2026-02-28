# Dockerfile for FastAPI Backend (Render-compatible)
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and titanic.csv
COPY backend ./backend
COPY titanic.csv ./titanic.csv

# Expose port (Render uses 10000 by default, but can be overridden)
EXPOSE 10000

# Start the backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]
