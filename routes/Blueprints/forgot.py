from flask import Blueprint, request, render_template, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer
from config.settings import EMAIL_USER, EMAIL_PASS, APP_URL, SECRET_KEY
from utils import email_utils
from models import user

forgot_bp = Blueprint('forgot', __name__)
serializer = URLSafeTimedSerializer(SECRET_KEY)
#ثراء\backend\templates\public\forgot_password.html


@forgot_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user_obj = user.get_by_id(email)
        if user_obj:
            token = serializer.dumps(email, salt='reset-password')
            email_utils.send_verification_email(email, token)
            flash('تم إرسال رابط إعادة التعيين إلى بريدك الإلكتروني.')
        else:
            flash('البريد غير مسجل لدينا.')
        return redirect(url_for('forgot.forgot_password_request'))
    return render_template('public/forgot_password.html')


@forgot_bp.route('/forgot_password/<token>', methods=['GET', 'POST'])
def forgot_password_page(token):
    try:
        email = serializer.loads(token, salt='reset-password', max_age=1800)
    except:
        return "الرابط منتهي أو غير صالح."

    if request.method == 'POST':
        new_password = request.form['password']
        user.update_password(email, new_password)
        flash('تم تعيين كلمة المرور الجديدة بنجاح.')
        return redirect(url_for('auth.login'))

    return render_template('public/forgot_password.html', email=email)


#يحتاج تعديلات بسيطة لربطه مع بقية التطبيق و غير جاهزة للاستخدام