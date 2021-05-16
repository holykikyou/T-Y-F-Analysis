from flask import Flask
app = Flask(__name__)  # 在当前文件下创建应用


@app.route("/")  # 装饰器，url，路由
def index():  # 试图函数
    return "hello world"


@app.route("/say_hello/<name>")  # 装饰器，url，路由
def say_hello(name):  # 试图函数
    return "hello world,I am your friend %s" % name

if __name__ == "__main__":
    app.run(debug=True)  # 运行app

    #app.run(host='0.0.0.0', port=80, debug=True)


#@app.route('/register', methods=['GET', 'POST'])
