#ثراء\backend\routes\Blueprints\admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db_thara import create_tables, get_connection
from config.settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from werkzeug.utils import secure_filename
from utils.m import login_required

import os
admin_bp = Blueprint('admin', __name__, url_prefix='/dashboard', template_folder='../../templates')


#UPLOAD_FOLDER = 'static/uploads'
# ضع هذا أعلى الملف
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# تأكد من وجود مجلد الرفع
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# ------------------ صفحة عرض جميع الخدمات ------------------
# ------------------ صفحة عرض جميع الخدمات ------------------
@admin_bp.route('/services')
@login_required
def admin_services():
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

    # تحويل كل tuple إلى dict ليعمل مع القالب
    services_data = [
        {
            'id': r[0],
            'title': r[1],
            'description': r[2],
            'price': r[3],
            'image_url': r[4],
            'delivery_time': r[5]
        } for r in rows
    ]

    return render_template('dashboard/services_dashboard.html', services=services_data)

# ------------------ صفحة إضافة خدمة جديدة ------------------

@admin_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        delivery_time = request.form['delivery_time']

        # --- التعامل مع الصورة المرفقة ---
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            # حفظ الصورة في مجلد uploads داخل static
            image_file.save(os.path.join(UPLOAD_FOLDER, filename))
            # مسار نسبي لقاعدة البيانات والعرض في القالب
            image_url = f'uploads/{filename}'
        else:
            image_url = 'uploads/default.jpg'  # صورة افتراضية

        # --- إدخال البيانات إلى قاعدة البيانات ---
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO services (title, description, price, image_url, delivery_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, price, image_url, delivery_time))
        conn.commit()
        cur.close()
        conn.close()

        flash('✅ تمت إضافة الخدمة بنجاح!', 'success')
        return redirect(url_for('admin.admin_services'))

    return render_template('dashboard/service_form.html', service=None)

# ------------------ صفحة تعديل خدمة ------------------
@admin_bp.route('/services/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required

def edit_service(service_id):
    conn = get_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form.get('image_url')
        delivery_time = request.form['delivery_time']

        cur.execute("""
            UPDATE services
            SET title=%s, description=%s, price=%s, image_url=%s, delivery_time=%s
            WHERE id=%s
        """, (title, description, price, image_url, delivery_time, service_id))
        conn.commit()

        cur.close()
        conn.close()
        flash('تم تحديث الخدمة بنجاح!', 'success')
        return redirect(url_for('admin.admin_services'))

    # عرض البيانات في النموذج للتعديل
    cur.execute("SELECT id, title, description, price, image_url, delivery_time FROM services WHERE id=%s", (service_id,))
    service = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('dashboard/service_form.html', service=service)

# ------------------ حذف خدمة ------------------
@admin_bp.route('/services/delete/<int:service_id>')
@login_required

def delete_service(service_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM services WHERE id=%s", (service_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('تم حذف الخدمة بنجاح!', 'danger')
    return redirect(url_for('admin.admin_services'))
