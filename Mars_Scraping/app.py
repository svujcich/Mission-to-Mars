#import tools
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
from datetime import datetime as dt

#set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#define route for HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#set up a scraping route (button that scrapes updated data when we tell it to)
#tied to a button that will run the code when its clicked
@app.route("/scrape")
def scrape(): #define the function
   mars = mongo.db.mars #assign a new variable that points to our Mongo database
   mars_data = scraping.scrape_all() #create a new variable to hold the newly scraped data
   mars.update_one({}, {"$set":mars_data}, upsert=True) #update db; insert data but not if an identical record already exists
   return redirect('/', code=302) #navigate back to see updated content
   #Summary: accesses the db, scrapes the data using scraping.py, return a message when succesful
   #upsert = true; mongo creates a new document if one does not already exist, new data will always be saved

   #tell Flask to run
if __name__ == "__main__":
   app.run()