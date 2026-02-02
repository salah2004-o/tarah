# settings.py
import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")  # غيّرها لأي مفتاح قوي
SESSION_TYPE = os.getenv("SESSION_TYPE", "filesystem")  # القيمة الافتراضية filesystem
# إعدادات البريد
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")  # استخدم كلمة مرور التطبيق من Gmail

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")  # كلمة المرور الافتراضية
DB_HOST = os.getenv("DB_HOST", "localhost")  # القيمة الافتراضية localhost
DB_PORT = os.getenv("DB_PORT", "5432")       # القيمة الافتراضية 5432

APP_URL = os.getenv("APP_URL")  # URL التطبيق، مثل http://localhost:5000
# إعدادات أخرى يمكن إضافتها هنا حسب الحاجة
