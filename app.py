import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():
        print([e for e in app.db.entries.find({})])
        if request.method == "POST":
            entry_content = request.form.get("content")     #see home.html with class="form" and class="content"
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            new_entry = {"content": entry_content, "date": formatted_date}
            app.db.entries.insert_one(new_entry)
        
        for entry in app.db.entries.find({}):
            entries.append(entry)

        # entries_with_date = [
        #     (
        #         entry[0],
        #         entry[1],
        #         datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d")
        #     )
        #     for entry in entries
        # ]
        # if you want to show the datetime in the format like Oct 13

        return render_template("home.html", entries=entries)
    return app