# ایمیج پایه پایتون
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# کپی بقیه فایل‌ها
COPY . .
ENV PYTHONUNBUFFERED=1

# دستور اجرای برنامه
CMD ["python", "main.py"]
