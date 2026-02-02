from database import db_thara
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    def __init__(self, id=None, username=None, email=None, name=None, password_hash=None, role='user',
                 profile_image=None, last_login=None, status='active', created_at=None, updated_at=None, is_verified=False):
        self.id = id
        self.username = username
        self.email = email
        self.name = name
        self.password_hash = password_hash  # كلمة المرور مشفرة
        self.role = role
        self.profile_image = profile_image
        self.last_login = last_login
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_verified = is_verified

    # ------------------------- إضافة مستخدم جديد -------------------------
    def add_user(self, raw_password):
        """إضافة مستخدم جديد مع تشفير كلمة المرور"""
        conn = db_thara.get_connection()
        cur = conn.cursor()
        hashed_password = generate_password_hash(raw_password)

        cur.execute("""
            INSERT INTO users (username, email, name, password_hash, role, profile_image, last_login, status, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (self.username, self.email, self.name, hashed_password, self.role,
              self.profile_image, self.last_login, self.status, self.is_verified))

        self.id = cur.fetchone()[0]
        self.password_hash = hashed_password
        conn.commit()
        cur.close()
        conn.close()
        return self.id

    # ------------------------- استرجاع مستخدم بالمعرف -------------------------
    @staticmethod
    def get_by_id(user_id):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, email, name, password_hash, role, profile_image, last_login, status,
                   created_at, updated_at, is_verified
            FROM users WHERE id = %s;
        """, (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                name=row[3],
                password_hash=row[4],
                role=row[5],
                profile_image=row[6],
                last_login=row[7],
                status=row[8],
                created_at=row[9],
                updated_at=row[10],
                is_verified=row[11]
            )
        return None

    # ------------------------- التحقق من بيانات الدخول -------------------------
    @staticmethod
    def authenticate(email, password, role=None):
        """التحقق من البريد وكلمة المرور، مع التحقق من الدور إذا تم تمريره"""
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, email, name, password_hash, role, profile_image, last_login, status,
                   created_at, updated_at, is_verified
            FROM users WHERE email = %s;
        """, (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                name=row[3],
                password_hash=row[4],
                role=row[5],
                profile_image=row[6],
                last_login=row[7],
                status=row[8],
                created_at=row[9],
                updated_at=row[10],
                is_verified=row[11]
            )
            # تحقق كلمة المرور
            if check_password_hash(user.password_hash, password):
                # تحقق الدور إذا تم تمريره
                if role is None or user.role == role:
                    return user
        return None
    @staticmethod
    def authenticate_admin(email, password):
        """التحقق من بيانات دخول المسؤول"""
        return User.authenticate(email, password, role='admin')
    
    # ------------------------- تحديث بيانات المستخدم -------------------------
    def update(self, update_password=False, raw_password=None):
        """تحديث بيانات المستخدم. إذا update_password=True سيتم تشفير كلمة المرور الجديدة"""
        conn = db_thara.get_connection()
        cur = conn.cursor()
        now = datetime.now()

        if update_password and raw_password:
            self.password_hash = generate_password_hash(raw_password)

        cur.execute("""
            UPDATE users
            SET username = %s, email = %s, name = %s, password_hash = %s,
                role = %s, is_verified = %s, updated_at = %s
            WHERE id = %s;
        """, (self.username, self.email, self.name, self.password_hash,
              self.role, self.is_verified, now, self.id))
        conn.commit()
        cur.close()
        conn.close()
    
    def update_admin(self, **kwargs):
        self.role = 'admin'
        self.update(**kwargs)
    # ------------------------- حذف المستخدم -------------------------
    def delete(self):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s;", (self.id,))
        conn.commit()
        cur.close()
        conn.close()
    
    # ------------------------- تحديث آخر تسجيل دخول -------------------------
    def update_last_login(self):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        now = datetime.now()
        cur.execute("""
            UPDATE users
            SET last_login = %s
            WHERE id = %s;
        """, (now, self.id))
        conn.commit()
        cur.close()
        conn.close()
    @staticmethod
    def get_by_email(email):
        """جلب المستخدم بواسطة البريد الإلكتروني"""
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, email, name, password_hash, role, profile_image, last_login, status,
                   created_at, updated_at, is_verified
            FROM users WHERE email = %s;
        """, (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                name=row[3],
                password_hash=row[4],
                role=row[5],
                profile_image=row[6],
                last_login=row[7],
                status=row[8],
                created_at=row[9],
                updated_at=row[10],
                is_verified=row[11]
            )
        return None
