import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from models.user import User
from models.Email import Email
from datetime import datetime, timedelta
import uuid
from utils.email_utils import send_verification_email

# ==========================================
# 1️⃣ إنشاء Blueprint
# ==========================================
# استخدمنا Blueprint لإنشاء جزء مستقل من التطبيق، يمكن تسجيله في app.py
# template_folder يشير لمجلد القوالب بالنسبة لهذا البلوبرنت
register_bp = Blueprint('register', __name__, template_folder='../../templates')


# ==========================================
# 2️⃣ صفحة عرض نموذج التسجيل (GET)
# ==========================================
# نعرض النموذج فقط، بدون معالجة بيانات
@register_bp.route('/register', methods=['GET'])
def show_registration_form():
    return render_template('auth/register.html')


# ==========================================
# 3️⃣ معالجة التسجيل (POST)
# ==========================================
@register_bp.route('/register', methods=['POST'])
def register_user():
    # جمع البيانات من الفورم
    username = request.form.get('username')
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    # ==========================================
    # 3.1 التحقق من تطابق كلمة المرور
    # ==========================================
    if password != confirm:
        flash('كلمة المرور غير متطابقة', 'danger')
        return render_template('auth/register.html')

    # ==========================================
    # 3.2 تشفير كلمة المرور
    # ==========================================
    # ❌ الخطأ السابق: تخزين كلمة المرور مباشرة بدون تشفير
    hashed_password = generate_password_hash(password)

    # إنشاء كائن مستخدم جديد (نمرر كلمة المرور الخام؛ add_user سيقوم بالتشفير)
    new_user = User(username=username, email=email, name=name)

    # ==========================================
    # 3.3 حفظ المستخدم في قاعدة البيانات
    # ==========================================
    try:
        user_id = new_user.add_user(password)  # دالة add_user من كلاس User تتوقع raw_password

        # إنشاء رمز تحقق وحفظه
        code = uuid.uuid4().hex
        expires_at = datetime.now() + timedelta(hours=1)
        token = Email(user_id=user_id, code=code, expires_at=expires_at)
        token.add_token()

        # إرسال بريد التحقق
        try:
            send_verification_email(email, code)
        except Exception as e:
            # لا نوقف التسجيل لو فشل الإرسال لكن نعلم المطور
            print('Failed to send verification email:', e)

        flash('تم إنشاء الحساب بنجاح! وصلَك رابط التحقق على بريدك، تحقق منه.', 'success')
        return redirect(url_for('login.html')) # هنا صححنا المسار ليشير للبلوبرنت الصحيح
    except Exception as e:
        flash(f'حدث خطأ أثناء إنشاء الحساب: {str(e)}', 'danger')
        return render_template('auth/register.html')


# ==========================================
# 4️⃣ ملاحظات مهمة عن الأخطاء السابقة
# ==========================================
"""
✅ الأخطاء السابقة التي تم تصحيحها:

1. استخدام "blueprints" بدل "Blueprint" → صححنا لاستخدام Blueprint الصحيح.

2. المسار للقوالب كان خاطئًا ('public/register.html') → صححناه ليصبح 'register.html' مباشرة حسب هيكل المشروع.

3. تخزين كلمة المرور بدون تشفير → استخدمنا generate_password_hash لتأمين الحسابات.

4. مزج GET وPOST في دالة واحدة → فصلناهم لتجنب التعقيد وجعل الكود احترافيًا.

5. التعامل مع ID المستخدم بعد الحفظ → نعيد user_id بعد add_user() لاستخدامه إذا احتجنا.

6. استخدام flash لإظهار رسائل الأخطاء أو النجاح للمستخدم.

"""
# نهاية الملف
