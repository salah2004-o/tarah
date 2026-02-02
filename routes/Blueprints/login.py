
from flask import Blueprint, render_template, request, session, redirect, url_for
from datetime import datetime
import pytz
from models.Email import Email
from models.user import User
from config.settings import EMAIL_PASS, EMAIL_USER
# ==============================

login_bp = Blueprint('login', __name__, template_folder='../../templates')

# ------------------------- صفحة تسجيل الدخول -------------------------
@login_bp.route('/login', methods=['GET'])
def login():


    tz = pytz.timezone("Africa/Tripoli")
    now = datetime.now(tz)
    current_time = now.strftime("%Y-%m-%d")
    
    
    

    return render_template('auth/login.html', current_time=current_time)


# ------------------------- معالجة تسجيل الدخول -------------------------
@login_bp.route('/login', methods=['POST'])
def handle_login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template('auth/login.html', error="يرجى إدخال البريد وكلمة المرور.")
      
        user = User.authenticate(email, password)
        if not user:
            return render_template('auth/login.html', error="بيانات الدخول غير صحيحة.")

        # التحقق من حالة البريد الإلكتروني (لغير الإدمن فقط)
        if not user.is_verified and user.role != 'admin':
            return render_template('auth/login.html', error="يرجى التحقق من بريدك الإلكتروني قبل تسجيل الدخول.")

        # تحديث آخر تسجيل دخول
        user.update_last_login()

        # تخزين المستخدم في الجلسة
        session['user_id'] = user.id
        session['user_role'] = user.role
        session['username'] = user.username

        # إعادة توجيه حسب الدور
        if user.role == 'admin':
            return redirect(url_for('admin.admin_services'))
        else:
            return redirect(url_for('server')) 
    except Exception as e:
        print("Login error:", e)
        return render_template('auth/login.html', error="حدث خطأ أثناء محاولة تسجيل الدخول.")

# ------------------------- صفحة الهبوط بعد تسجيل الدخول -------------------------
@login_bp.route('/landing')
def landing_page():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))


    # اسم المستخدم من session
    username = session.get('username', 'ضيف')

    # الوقت الحالي حسب منطقتك
    tz = pytz.timezone("Africa/Tripoli")
    now = datetime.now(tz)
    current_time = now.strftime("%Y-%m-%d")

    # تحديد التحية حسب الوقت
    hour = now.hour
    if 5 <= hour < 12:
        greeting = "صباح الخير"
    elif 12 <= hour < 17:
        greeting = "مساء النور"
    else:
        greeting = "مساء الخير"

    # إرسال المعلومات للصفحة
    return render_template(
        'public/landing.html',
        username=username,
        greeting=greeting,
        current_time=current_time
    )
# ------------------------- صفحة حساب المستخدم -------------------------
@login_bp.route("/account")
def account():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    user = User.get_by_id(session['user_id'])
    return render_template('public/account.html', user=user)


@login_bp.route("/account/settings", methods=['GET', 'POST'])
def account_settings():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    user = User.get_by_id(session['user_id'])

    if request.method == 'POST':
        # معالجة تحديث الإعدادات هنا
        name = request.form.get('name')
        email = request.form.get('email')
        user.username = name
        user.email = email
        user.update()  # تحديث البيانات في قاعدة البيانات
        return redirect(url_for('login.account_settings'))

    return render_template('public/account_settings.html', user=user)



# ------------------------- التحقق من البريد الإلكتروني -------------------------
@login_bp.route('/verify_email/<code>')
def verify_email(code):
    try:
        # تنظيف الرموز القديمة قبل التحقق
        Email().delete_old_tokens()

        # جلب الرمز من قاعدة البيانات
        email_token = Email.get_by_code(code)
        if email_token and not email_token.is_used and email_token.expires_at > datetime.now():
            # الرمز صالح وغير مستخدم
            user = User.get_by_id(email_token.user_id)
            if user:
                user.is_verified = True
                user.update()
                email_token.mark_as_used()
                return render_template('public/verify_success.html', user=user)

        # الرمز غير صالح أو مستخدم أو منتهي
        return render_template('public/verify_failure.html')

    except Exception as e:
        print("Email verification error:", e)
        return render_template('public/verify_failure.html')
