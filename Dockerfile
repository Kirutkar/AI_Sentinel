FROM python:3.10-slim

WORKDIR /app

# Upgrade pip + resolver
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

# Force pip to use simpler resolver
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "10000", "--server.address", "0.0.0.0"]