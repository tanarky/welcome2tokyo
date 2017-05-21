# coding: utf-8
from flask import Flask, render_template
from admin import app_admin

app = Flask(__name__)
app.secret_key = 'tanarky'
app.debug = True
app.register_blueprint(app_admin)

@app.route('/')
def doc_root():
    return render_template('pages_top.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
