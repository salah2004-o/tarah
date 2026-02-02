# ثراء\backend\app.py
import os, json
from flask import Flask, render_template, abort, sessions, session, redirect, url_for
from routes.Blueprints.register import register_bp  # بلوبرنت التسجيل
from routes.Blueprints.login import login_bp  # بلوبرنت تسجيل الدخول
from routes.Blueprints.admin import admin_bp  # بلوبرنت لوحة تحكم المسؤول
from routes.Blueprints.forgot import forgot_bp
import pytz
from datetime import datetime
from config.settings import SECRET_KEY  # إعدادات التطبيق
from utils.m import login_required
from database.db_thara import get_connection

# ==============================
# 1️⃣ إنشاء التطبيق
# ==============================
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = SECRET_KEY # استخدم مفتاح قوي أو من config

# ==============================
# 2️⃣ تسجيل البلوبرنت
# ==============================
app.register_blueprint(admin_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(forgot_bp)
# ==============================
# 3️⃣ الصفحة الرئيسية
# ==============================

@app.route("/") #صفحة العرض الاساسية للمستخدم
def h():
    return render_template("public/index.html")


@app.route("/server")
@login_required
def server():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, description, price, image_url, delivery_time
        FROM services
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    services_data = [
    {
        'id': r[0],
        'title': r[1],
        'description': r[2],
        'price': r[3],
        'image_url': r[4] or 'default.jpg',  # <-- صورة افتراضية
        'delivery_time': r[5]
    } for r in rows
    ]


    return render_template("public/services.html", services=services_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('h'))

@app.route('/profile') #صفحة عننا فيها تعريف الشركة
def profile():
    return render_template('public/profile.html')

# ==============================
# 4️⃣ دالة لقراءة الصفحات
# ==============================
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'pages.json')

def load_pages():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

# ==============================
# 5️⃣ route للصفحات حسب slug
# ==============================
@app.route('/<slug>')
def show_page(slug):
    pages = load_pages()
    page = next((p for p in pages if p.get('slug') == slug), None)
    if not page:
        abort(404)
    return render_template('shared/page.html', page=page)


from models import user

def create_admin():
    email = "thaaraaa190@gmail.com"
    password = "IOP_890i"  # كلمة المرور الأصلية
    admin = user.User.get_by_email(email)

    if admin:
        print("⚠️ الأدمن موجود مسبقًا:", email)
        return

    new_admin = user.User(
        username="adminn",
        name="thara",
        email=email,
        role="admin",
        is_verified=True
    )
    
    # تشفير كلمة المرور وإضافة المستخدم
    new_admin.add_user(password)
    print("✅ تم إنشاء الأدمن بنجاح:", email)

if __name__ == "__main__":
    create_admin()
# ==============================
# 4️⃣ تشغيل السيرفر
# ==============================
if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")

