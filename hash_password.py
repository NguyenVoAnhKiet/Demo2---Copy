import hashlib
import sqlite3


# Hàm băm SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect("instance/DemoDB")
cursor = conn.cursor()

# Truy vấn để lấy mật khẩu cần băm
cursor.execute("SELECT user_id, password FROM users")
rows = cursor.fetchall()

# Cập nhật mật khẩu đã băm vào cơ sở dữ liệu
for row in rows:
    id = row[0]
    password = row[1]
    if password:  # Kiểm tra nếu mật khẩu không rỗng
        hashed_password = hash_password(password)
        cursor.execute(
            "UPDATE users SET password = ? WHERE user_id = ?", (hashed_password, id)
        )

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
