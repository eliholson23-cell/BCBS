from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('launch_page.html')

@app.route('/data_review')
def data_review():
    return send_file('launch_page.html')

@app.route('/bucketing')
def bucketing():
    return send_file('launch_page.html')

@app.route('/email')
def email():
    return send_file('launch_page.html')

@app.route('/launch')
def launch():
    return send_file('launch_page.html')

if __name__ == '__main__':
    app.run(debug=True)