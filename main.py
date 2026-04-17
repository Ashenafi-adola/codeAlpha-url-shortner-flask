from flask import Flask
from flask import render_template, request
import requests
import os
import dotenv

dotenv.load_dotenv()


app = Flask(__name__)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

@app.route("/", methods=['POST', 'GET'])
def index():
    short_url = None
    if request.method == "POST":
        original_url = request.form['original']
        short_url = url_shortener(original_url)

    return render_template('index.html', short_url=short_url)

@app.route("/url-list/")
def urlLists():
    return "URl lists"

def url_shortener(original_url):
    base_url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": f'Bearer {ACCESS_TOKEN}'
    }
    try:
        response = requests.post(base_url, headers=headers, json={'long_url':original_url})
        if response.status_code == 200:
            return response.json()['link']
        else:
            return None
    except requests.ConnectTimeout:
        return f'{requests.ConnectTimeout}'