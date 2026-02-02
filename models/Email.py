#ملف البريد الإلكتروني
from datetime import datetime
from database import db_thara

class Email:
    def __init__(self, id=None, user_id=None, code=None, expires_at=None, is_used=False, created_at=None): 
        self.id = id
        self.user_id = user_id
        self.code = code
        self.expires_at = expires_at
        self.is_used = is_used
        self.created_at = created_at

    # إضافة رمز تحقق جديد
    def add_token(self):

        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO email_verification_tokens (user_id, code, expires_at, is_used)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """, (self.user_id, self.code, self.expires_at, self.is_used))
        self.id = cur.fetchone()[0] # الحصول على معرف الرمز الجديد
        conn.commit()
        cur.close()
        conn.close()
    # استرجاع رمز تحقق بواسطة الكود
    @staticmethod
    def get_by_code(code):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, user_id, code, expires_at, is_used, created_at
            FROM email_verification_tokens WHERE code = %s;""", (code,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return Email(*row) if row else None
    # تحديث حالة الرمز (مستخدم أو لا)
    def mark_as_used(self):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE email_verification_tokens
            SET is_used=TRUE
            WHERE id = %s;
            """, (self.id,))
        conn.commit()
        cur.close()
        conn.close()
    # حذف الرموز القديمة (منتهية الصلاحية أو المستخدمة)
    def delete_old_tokens(self):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM email_verification_tokens
            WHERE expires_at < %s OR is_used=TRUE;
            """, (datetime.now(),))
        conn.commit()
        cur.close()
        conn.close()
# نهاية ملف البريد الإلكتروني