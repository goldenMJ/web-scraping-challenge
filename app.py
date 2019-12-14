from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Missions_to_Mars
import requests

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)


@app.route("/")
@app.route('/index')
def index():
    mars = mongo.db
    use_col = mars['items']
    items = use_col.find_one()
    return render_template("/index.html", items=items)



@app.route("/scrape")
def scraper():
    mars = mongo.db
    use_col = mars['items']
    mars_data = Missions_to_Mars.scrape()
    print(type(mars_data))
    use_col.insert_one(mars_data)
    return redirect("/index", code=302)


if __name__ == "__main__":
    app.run(debug=True)
