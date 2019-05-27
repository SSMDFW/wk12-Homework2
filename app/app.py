
import scrape_mars as sm
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect

app = Flask(__name__)

#create mongo connection
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)
# db = client.mars_db
# collection = db.mars_data_entries
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



# @app.route("/")
# def index():
#     mars_data = list(db.collection.find())[0]
#     return  render_template('.\\templates\\index.html', mars_data=mars_data)

# @app.route("/scrape")
# def web_scrape():
#     db.collection.remove({})
#     mars_data = sm.scrape_mars()
#     db.collection.insert_one(mars_data)
#     return "Scraping Worked!"
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = sm.scrape_mars()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Worked!"


if __name__ == "__main__":
    app.run(debug=True)