FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

ENV PYTHONPATH="/app:$PYTHONPATH"

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint_python_runner.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
