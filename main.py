from flask import Flask
from flask import render_template, request
import requests

app = Flask(__name__)
ACCESS_TOKEN = "08bf2d660ee4a94367096f80127de64a7848cb91"


name = "ashenafi"
@app.route("/", methods=['POST', 'GET'])
def index():
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