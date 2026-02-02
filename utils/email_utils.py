import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import EMAIL_USER, EMAIL_PASS, APP_URL


def send_verification_email(to_email, code):
    if not EMAIL_USER or not EMAIL_PASS or not APP_URL:
        raise RuntimeError('Email credentials or APP_URL not configured in environment')

    subject = 'تأكيد البريد الإلكتروني - الثراء'
    verify_link = f"{APP_URL}/verify_email/{code}"

    html = f"""
<html lang="ar" dir="rtl">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body style="margin:0; padding:0; background-color: #052c25; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <table align="center" width="100%" cellpadding="0" cellspacing="0" 
           style="max-width:600px; margin:40px auto; background-color:#f5f1eb; 
                  border-radius:24px; overflow:hidden; box-shadow:0 15px 50px rgba(0,0,0,0.4);
                  border: 2px solid #c9a66b;">
      
      <tr>
        <td style="background-color: #052c25; padding:50px 20px; text-align:center; border-bottom: 4px solid #c9a66b;">
          <h1 style="color:#c9a66b; margin:0; font-size:42px; font-weight:bold; letter-spacing: 2px;">
            الثراء
          </h1>
          <p style="color:#f5f1eb; margin:10px 0 0 0; font-size:16px; opacity: 0.8;">
            نحو تميز رقمي بلا حدود
          </p>
        </td>
      </tr>
      
      <tr>
        <td style="padding:40px 35px; color:#052c25; font-size:16px; line-height:1.8; text-align: right;">
          <h2 style="color:#052c25; font-size:26px; margin-bottom:25px; text-align:center; font-weight: bold;">
            أهلاً بك في عالم الثراء! ✨
          </h2>
          
          <p style="margin-bottom:20px; font-size: 18px;">
            مرحباً <strong></strong>،
          </p>
          
          <p style="margin-bottom:25px;">
            يسعدنا انضمامك إلى <span style="color:#c9a66b; font-weight: bold;">وكالة الثراء</span>. أنت الآن على بعد خطوة واحدة من الانطلاق في رحلة فريدة لتحويل أفكارك إلى نتائج ملموسة. لتفعيل حسابك والبدء، يرجى تأكيد بريدك الإلكتروني:
          </p>
          
          <table width="100%" cellpadding="0" cellspacing="0" style="margin:45px 0;">
            <tr>
              <td align="center">
                <a href="{verify_link}" 
                   style="background: #c9a66b; 
                          color:#052c25; text-decoration:none; 
                          padding:18px 50px; border-radius:15px; 
                          display:inline-block; font-weight:bold; font-size:20px;
                          box-shadow: 0 8px 20px rgba(201, 166, 107, 0.3);
                          transition: all 0.3s ease;">
                  تفعيل حسابي الآن
                </a>
              </td>
            </tr>
          </table>
          
          <div style="background-color:#ffffff; padding:20px; border-radius:15px; 
                      margin:35px 0; border: 1px solid #ddd; border-right: 5px solid #c9a66b;">
            <p style="margin:0; font-size:13px; color:#777;">
              <strong>إذا واجهت مشكلة في الزر، انسخ هذا الرابط في متصفحك:</strong>
            </p>
            <p style="margin:12px 0 0 0; word-break:break-all; direction:ltr; text-align:left; font-size: 14px;">
              <a href="{verify_link}" style="color:#c9a66b; text-decoration:none;">
                {verify_link}
              </a>
            </p>
          </div>
          
          <div style="background-color:#fff9ee; padding:15px; border-radius:12px;
                      margin:25px 0; border-right: 4px solid #ffc107;">
            <p style="margin:0; font-size:14px; color:#856404; line-height: 1.6;">
              <strong>🛡️ ملاحظة أمنية:</strong><br>
              إذا لم تقم بطلب التسجيل في وكالة الثراء، يمكنك ببساطة تجاهل هذا البريد. لن يتم تفعيل أي حساب دون النقر على الرابط أعلاه.
            </p>
          </div>
          
          <p style="color:#052c25; font-size:17px; margin-top:40px; font-weight:bold; border-top: 1px solid #eee; padding-top: 25px;">
            بكل ود،<br>
            <span style="color:#c9a66b;">فريق وكالة الثراء</span>
          </p>
        </td>
      </tr>
      
      <tr>
        <td style="background-color: #052c25; padding:35px 20px; text-align:center; color:#f5f1eb;">
          <p style="margin:0 0 15px 0; font-size: 14px; opacity: 0.9;">
            © 2026 <strong>وكالة الثراء</strong>. جميع الحقوق محفوظة.
          </p>
          
          <p style="margin:20px 0;">
            <a href="#" style="color:#c9a66b; text-decoration:none; margin:0 10px;">Twitter</a> • 
            <a href="#" style="color:#c9a66b; text-decoration:none; margin:0 10px;">Instagram</a> • 
            <a href="#" style="color:#c9a66b; text-decoration:none; margin:0 10px;">LinkedIn</a>
          </p>

          <p style="margin:20px 0 0 0; font-size:12px; opacity: 0.7;">
            لقد استلمت هذا البريد لأنك قمت بالتسجيل في موقعنا.<br>
            المملكة العربية السعودية | <a href="{APP_URL}/privacy" style="color:#c9a66b;">سياسة الخصوصية</a>
          </p>
        </td>
      </tr>
    </table>
    
    <div style="height:50px;"></div>
  </body>
</html>
"""
    # إنشاء الرسالة
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"الثراء <{EMAIL_USER}>"
    msg['To'] = to_email

    part = MIMEText(html, 'html', 'utf-8')
    msg.attach(part)

    # إعدادات SMTP الخاصة بـ Gmail
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    email_user = EMAIL_USER
    email_pass = EMAIL_PASS
    # إرسال البريد
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
            print(f"✅ تم إرسال بريد التأكيد بنجاح إلى: {to_email}")
    except smtplib.SMTPException as e:
        print(f"❌ خطأ في إرسال البريد: {str(e)}")
        raise RuntimeError(f"Failed to send email: {str(e)}")

