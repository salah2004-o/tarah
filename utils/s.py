from models.user import User
from werkzeug.security import generate_password_hash

admins = [
    {
        "username": "صلاح",
        "email": "admin1@example.com",
        "password": "admin123"
    },
    {
        "username": "حذيفه",
        "email": "admin2@example.com",
        "password": "admin456"
    }
]

for data in admins:
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role='admin',
        is_verified=True
    )
    user.save()

print("✅ تم إنشاء الإدمنات بنجاح!")
