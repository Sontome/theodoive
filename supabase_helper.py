from supabase import create_client
import bcrypt
from supabase_config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_account(username, password):
    try:
        res = supabase.table("users").select("username").eq("username", username).execute()
        if res.data:
            return False, "🛑 Tên tài khoản đã tồn tại"

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        supabase.table("users").insert({
            "username": username,
            "password": hashed_pw
        }).execute()
        return True, "✅ Tạo tài khoản thành công"
    except Exception as e:
        return False, f"❌ Lỗi tạo tài khoản: {e}"

def check_login(username, password):
    try:
        res = supabase.table("users").select("*").eq("username", username).eq("status", "active").execute()
        if res.data:
            user_data = res.data[0]
            return bcrypt.checkpw(password.encode(), user_data["password"].encode())
        return False
    except Exception as e:
        print("Lỗi check login:", e)
        return False