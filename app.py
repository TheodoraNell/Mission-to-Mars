from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Add the next route and function
@app.route("/scrape")
def scrape():
   # assign a new variable that points to the Mongo database
   mars = mongo.db.mars
   # create a variable to hole newly-scraped data using scrape_all() function
   mars_data = scraping.scrape_all()
   # update the database with newly gathered data
   # update_one() syntax:  .update_one(query_parameter, {"$set": data}, options)
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

   # Tell Flask to run
   if __name__ == "__main__":
   app.run()

