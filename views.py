from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, exc
import pdb
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
      print("Problem commiting the update in {0}".format(new_restaurant.name))
      print("Error message:".format(e.message))


    return jsonify(new_restaurant.serialize)
  elif request.method == 'GET':
    # Return all Restaurants
    restaurants = session.query(Restaurant)
    restaurants_list = []
    # add serialized json to array
    for res in restaurants:
      restaurants_list.append(res.serialize)

    # send back a restaurants json object, with it's value the array of json restaurants
    return_obj={}
    return_obj['restaurants']=restaurants_list
    return jsonify(return_obj)
    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  # get the restaurant
  try:
    restaurant=session.query(Restaurant).filter_by(id=id).one()
    res_string = ""
    if restaurant:
      if request.method == 'GET':
        print('GET method')
        res_string = jsonify(restaurant.serialize)
      elif request.method == 'PUT':
        # restaurant_name = request.form.get('name','')
        restaurant_name = request.args.get('name')
        if restaurant_name == '':
          res_string = "name not found in form"
        else:
          print("Changing name from {0} to {1}".format(restaurant.restaurant_name, restaurant_name))
          restaurant.restaurant_name=restaurant_name
          try:
            session.add(restaurant)
            session.commit()
          except exc.DatabaseError as e:
            print("Problem commiting the update in {0}. name not changed to {0}".format(restaurant.restaurant_name, restaurant_name))
            print("Error message:".format(e.message))
            pass
          res_string = jsonify(restaurant.serialize)
        print('PUT method')
      elif request.method == 'DELETE':
        print('DELETE method')
        session.delete(restaurant)
        session.commit()
      else:
        print('Unsupported HTTP method')
    else:
      res_string = "restaurant {0} could not be found".format(id)
    return res_string
  except exc.SQLAlchemyError as e:
    print("Problem finding restaurant with ID: {0}".format(id))
    print("Error message:".format(e.message))
    return "Problem finding restaurant with ID: {0} \n".format(id)
  # print(request.headers)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
