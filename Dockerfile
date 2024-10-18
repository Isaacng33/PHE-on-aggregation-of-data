FROM python:3.9


WORKDIR /app

# Install system dependencies for building packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gcc \
    g++ \
    python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3.9", "-m", "run"]