# اختيار نظام تشغيل فيه بايثون جاهز
FROM python:3.10-slim

# تحديث السيرفر وتنصيب Tesseract والـ Libraries بتاعته
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# تحديد الفولدر اللي الكود هيعيش فيه جوه السيرفر
WORKDIR /app

# نسخ ملف المكتبات (requirements) عشان ينصبها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل ملفات مشروعك (app.py و payment_ai.py وغيرهم)
COPY . .

# الأمر اللي بيشغل السيرفر (تأكدي إن اسم ملف التشغيل app.py)
CMD ["python", "app.py"]