FROM python:3.9

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

CMD ["sh", "-c", "PYTHONPATH=/src uvicorn api.main:app --host 0.0.0.0 --port 8000"]
