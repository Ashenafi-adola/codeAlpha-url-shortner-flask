from flask import Flask
from flask import render_template, request
import requests
import os
import dotenv
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
import sqlite3

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

app = Flask(__name__)
dotenv.load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "urls_db.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class UrlsStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), unique=True, nullable=False)
    shortened_url = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.shortened_url}'
    
    def __str__(self):
        return self.shortened_url

with app.app_context():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def index():
    short_url = None
    if request.method == "POST":
        original_url = request.form['original']
        short_url = url_shortener(original_url)
        new_url = UrlsStore(original_url=original_url, shortened_url=short_url)
        try:
            db.session.add(new_url)
            db.session.commit()
        except:
            pass
    return render_template('index.html', short_url=short_url)

@app.route("/url-list/")
def urlLists():
    urls = UrlsStore.query.all()
    return render_template('urlsList.html', urls=urls)

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