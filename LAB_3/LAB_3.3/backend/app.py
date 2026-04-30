from flask import Flask, render_template
from router import router
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Bật CORS để React (port 3000) gọi được Flask (port 5000)

app.register_blueprint(router) # Đăng ký router chứa API

@app.route("/")
def index():
    return render_template("employees.html")

if __name__ == "__main__":
    app.run(debug=True)