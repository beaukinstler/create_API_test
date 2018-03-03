from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




#foursquare_client_id = ''

#foursquare_client_secret = ''

#google_api_key = ''

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  if request.method == 'POST':
    # expects params
    # location, mealType
    location = request.form.get('location','55108')
    mealType = request.form.get('mealType','Pizza')

    print location,mealType

    # find a restaurant   
    located_restaurant = findARestaurant(mealType, location)
    name = located_restaurant['name']
    address = located_restaurant['address']
    image = located_restaurant['image']
    # insert into db
    new_restaurant = Restaurant(restaurant_name=name,restaurant_address=address,restaurant_image=image)
    try:
      session.add(new_restaurant)
      session.commit()
    except exc.DatabaseError as e:
      print("Problem commiting the update in %s" % new_restaurant.name)
      print("Error message:" % e.message)
    # return json data

    return jsonify(new_restaurant.serialize)
  elif request.method == 'GET':
    # Return all Restaurants
    restaurants = session.query(Restaurant)
    res_string = ""

    for res in restaurants:
      res_string += str(res.restaurant_name) + "<br>"
      res_string += str(res.restaurant_address) + "<br>"
      res_string += str(res.restaurant_image) + "<br>"
      res_string += "<br>"

    return res_string
    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
  print(request.headers)
  return 'handler'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
