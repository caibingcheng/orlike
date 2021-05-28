from flask import Flask, render_template

app = Flask(__name__, static_folder='/')
@app.route('/test', methods=["GET"])
def style():
    return render_template("test.html", server="https://orlike-caibingcheng.vercel.app")

if __name__ == "__main__":
    app.run()