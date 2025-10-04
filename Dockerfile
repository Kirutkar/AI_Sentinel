FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "10000", "--server.address", "0.0.0.0"]
