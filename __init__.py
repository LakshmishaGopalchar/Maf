from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None

    return '''<h1>The language value is: {}</h1>'''.format(language)

app.debug = True
if __name__ == "__main__":
    app.run()
