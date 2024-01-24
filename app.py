import re
# 初始化資料庫連線
import pymongo
client=pymongo.MongoClient("mongodb+srv://zensean00:root0123@cluster0.ja4dnzc.mongodb.net/?retryWrites=true&w=majority")
db=client.member_system
print("資料庫連線建立成功")

# 初始化 Flask 伺服器
from flask import *
app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key="root0123"
# 首頁
@app.route("/")
def home():
    session.pop("email", None)
    return render_template("home.html")

# 登入錯誤頁面
@app.route("/loginError")
def loginError():
    session.pop("email", None)
    msg=request.args.get("msg", "發生錯誤，請聯繫客服")
    return render_template("loginError.html", msg=msg)

# 會員頁面
@app.route("/myAccount")
def myAccount():
    if "email" in session:
        # 從session中取得資訊
        email = session.get("email")
        nickname = session.get("nickname")
        # 傳遞資訊給HTML
        return render_template("myAccount.html", email=email, nickname=nickname)
    else:
        return redirect("/")

# 註冊頁面
@app.route("/createAccount")
def createAccount():
    return render_template("createAccount.html")

# 註冊錯誤頁面
@app.route("/error")
def error():
    msg=request.args.get("msg", "發生錯誤，請聯繫客服")
    return render_template("error.html", msg=msg)

@app.route("/myAccountData", methods=["POST"])
def myAccountData():
    # 從前端接收資料
    email=request.form["email"]
    password=request.form["password"]
    phoneNumber=request.form["phoneNumber"]
    nickname=request.form["nickname"]
    # 檢查 email 是否為有效的電子郵件格式
    if not is_valid_email(email):
       return redirect("/error?msg=請輸入有效的電子郵件地址")
    # 根據接收到的資料，和資料庫互動
    collection=db.user
    # 檢查會員集合中是否有相同 Email 的資料
    result=collection.find_one({
        "email":email
    })
    if result != None:
        return redirect("/error?msg=信箱已經被註冊")
    # 檢查密碼是否符合規則
    if not is_valid_password(password):
        return redirect("/error?msg=密碼需8個字元以上且第一個字元須為大寫英文")
    # 將資料存入 session
    session["signup_data"] = {
        "email": email,
        "password": password,
        "phoneNumber": phoneNumber,
        "nickname": nickname,
    }
    return redirect("/gender")

# 註冊性別頁面
@app.route("/gender")
def gender():
    return render_template("gender.html")

@app.route("/genderData", methods=["POST"])
def genderData():
    signup_data = session.get("signup_data")    # 從 session 中讀取資料
    gender = request.form["gender"]             # 從表單中獲取性別資料
    signup_data["gender"] = gender              # 將性別資料加入到完整的資料集中
    collection=db.user                          # 根據接收到的資料，和資料庫互動
    collection.insert_one(signup_data)          # 把資料放進資料庫，完成註冊
    session.pop("signup_data", None)            # 清除 session 中的資料
    return redirect("/")

# 登入頁面
@app.route("/signin", methods=["POST"])
def signin():
   # 從前端接收資料
    email=request.form["email"]
    password=request.form["password"]
    # 根據接收到的資料，和資料庫互動
    collection=db.user
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    # 找不到對應的資料，登入失敗，導向到錯誤頁面
    if result==None:
        return redirect("/loginError?msg=帳號或密碼錯誤，請重新輸入")
    # 登入成功，在 Session 紀錄會員資訊，導向到會員頁面
    session["email"]=result["email"]
    session["nickname"]=result["nickname"]
    return redirect("/myAccount")

    # 登出
    @app.route("/signout")
    def signout():
        del session["email"]
        del session["nickname"]
        return redirect("/")

def is_valid_email(email):
    # 檢查是否為有效的電子郵件格式
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))

def is_valid_password(password):
    # 密碼長度至少八個字元，第一個字為英文大寫
    pattern = re.compile(r"^[A-Z]\w{7,}$")
    return bool(re.match(pattern, password))

if __name__ == "__main__":
    app.run()