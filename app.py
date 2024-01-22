# 初始化資料庫連線
import pymongo
client=pymongo.MongoClient("mongodb+srv://zensean00:root1234@cluster0.ja4dnzc.mongodb.net/?retryWrites=true&w=majority")
db=client.member_system
print("資料庫連線建立成功")

# 初始化 Flask 伺服器
from flask import *
app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key=""
#處理路由
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/myaccount")
def myaccount():
    return render_template("myaccount.html")

@app.route("/error")
def error():
    msg=request.args.get("msg", "發生錯誤，請聯繫客服")
    return render_template("error.html", msg=msg)

app.run(port=3000)