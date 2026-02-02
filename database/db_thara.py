#ثراء\backend\database\db_thara.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import psycopg2
from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
# إعداد الاتصال بقاعدة البيانات
def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

# إنشاء الجداول
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(30) NOT NULL,
            email VARCHAR(60) UNIQUE NOT NULL,
            password_hash VARCHAR(260) NOT NULL,
            role VARCHAR(20) DEFAULT 'user', -- admin / user
            profile_image TEXT,
            last_login TIMESTAMP,
            status VARCHAR(20) DEFAULT 'active', -- active / suspended / deleted
            is_verified BOOLEAN DEFAULT FALSE, -- تحقق البريد
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # ---------------- PRODUCTS TABLE ---------------- هنا جدول المنتجات
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            image_url TEXT,
            delivery_time INTEGER, -- باليوم
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # ---------------- EMAIL VERIFICATION TOKENS TABLE ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS email_verification_tokens (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            code VARCHAR(100) UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            is_used BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    #----------------- services TABLE ---------------- هنا جدول الخدمات
    cur.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            image_url TEXT,
            delivery_time INTEGER, -- باليوم
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

     #----------------- orders TABLE ---------------- هنا جدول الطلبات
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("All tables created successfully.")
    print("تم إنشاء جميع الجداول بنجاح.")


