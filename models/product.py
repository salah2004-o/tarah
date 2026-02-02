#ملف المنتج
from datetime import datetime
from database import db_thara

class Product: #كلاس المنتجات 
    def __init__(self, id=None, name=None, description=None, price=None, stock=None,
                 image_url=None, user_id=None, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_url = image_url
        self.user_id = user_id
        self.created_at = created_at
    # إضافة منتج جديد
    def add_product(self):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO products (name, description, price, stock, image_url, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """, (self.name, self.description, self.price, self.stock, self.image_url, self.user_id))
        self.id = cur.fetchone()[0] # الحصول على معرف المنتج الجديد
        conn.commit()
        cur.close()
        conn.close()
    # استرجاع منتج بواسطة المعرف
    @staticmethod
    def get_all():
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, description, price, stock, image_url, user_id, created_at
            FROM products;
            """)
        rows = cur.fetchall() # استرجاع جميع الصفوف
        cur.close()
        conn.close()
        return [Product(*row) for row in rows] # تحويل كل صف إلى كائن Product
    #تحديث المنتج
    
    def update(self):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE products
            SET name = %s, description = %s, price = %s, stock = %s, image_url = %s, user_id = %s, created_at = %s
            WHERE id = %s;
            """, (self.name, self.description, self.price, self.stock, self.image_url, self.user_id, datetime.now(), self.id))
        conn.commit()
        cur.close() 
        conn.close()
    # حذف المنتج
    def delete(self):
        conn = db_thara.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id = %s;", (self.id,))
        conn.commit()
        cur.close()
        conn.close()

    