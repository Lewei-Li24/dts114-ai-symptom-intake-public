FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY Task1/generated_project/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY Task1/generated_project/ ./

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
