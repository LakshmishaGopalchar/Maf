from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello Azure!</h1>"

app.debug = True
if __name__ == "__main__":
    app.run()
