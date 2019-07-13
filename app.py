# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import scrape_mars
import os

# Create an instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/app"
mongo = PyMongo(app)

# Create route for index.html and find documents from mongo
@app.route("/")
def home(): 

    # Get data
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scraped functions
    mars_data = mongo.db.mars_data
    mars_scrape = scrape_mars.scrape_mars_news()
    mars_scrape = scrape_mars.scrape_mars_image()
    mars_scrape = scrape_mars.scrape_mars_facts()
    mars_scrape = scrape_mars.scrape_mars_weather()
    mars_scrape = scrape_mars.scrape_mars_hemispheres()
    mars_data.update({}, mars_scrape, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)