# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/app"
mongo = PyMongo(app)

@app.route("/")
def index(): 
    mars = mongo.db.mars.find_one()
    print(mars['mars_weather_tweet'])
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_info = scrape_mars.scrape_info()
    mars.update({}, mars_info, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)