# IBM Code Engine Containerfile
# Base: UBI 9 Minimal (IBM Red Hat Universal Base Image) or Official Python Slim
FROM registry.access.redhat.com/ubi9/python-310:latest

WORKDIR /app

# Switch to root for system package updates
USER 0

# Copy requirements
COPY requirements.txt .

# Install dependencies strictly using pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ ./app/
COPY orchestration/ ./orchestration/
COPY tests/ ./tests/
COPY run.py .

# Switch back to non-root user (1001) for IBM Cloud security compliance
USER 1001

EXPOSE 8000

ENV PORT=8000 \
    HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1

CMD ["python", "run.py"]
