from flask import Blueprint, render_template, session
import pytz
from datetime import datetime
import psycopg2
from config.settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

public_bp = Blueprint('public', __name__, url_prefix='/')

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

@public_bp.route('/services')
def services():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, description, price, image_url, delivery_time 
        FROM services
        ORDER BY created_at DESC
    """)
    services_data = cur.fetchall()
    cur.close()
    conn.close()

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


    return render_template('public/services.html', services=services_data,
        username=username,
        greeting=greeting,
        current_time=current_time
        )
