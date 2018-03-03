"""
This file stores the comman db functions
to access the database with the app.
"""
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, BASE

engine = create_engine('sqlite:///restaurants.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
BASE.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
ses = DBSession()


# db update function
def update_item(object_name):
    """
    Take and object, and update it in the database
    """
    try:
        ses.add(object_name)
        ses.commit()
    except exc.DatabaseError as e:
        print("Problem commiting the update in %s" % object_name.name)
        print("Error message:" % e.message)

# Print out all the restaurants
def list_all_restaurants():
    """
    List all restaurants by name and id, order based on data table
    """
    
    restaurants = ses.query(Restaurant)

    for restaurant in restaurants:
        print("Name: {}, ID: {}".format(str(restaurant.name), str(restaurant.id)))


def get_all_restaurants():
    """
    Get all restaurants by name and id, order based on data table
    Returns: An iterable list of restaurant objects
    """
    
    return ses.query(Restaurant)


# Find restaurant by ID
def get_restaurant(id_to_find):
    """ Using and id number, return Restaurant object """

    restaurant = ses.query(Restaurant).filter_by(id=id_to_find).one()
    return restaurant


# Add a new restaurant
def add_restaurant(restaurant_name):
    """

    """

    restaurant = Restaurant(restaurant_name=restaurant_name)
    ses.add(restaurant)
    ses.commit()
    new_restaurant = \
        ses.query(Restaurant).filter_by(restaurant_name=restaurant_name).one()
    return new_restaurant.id


# Delete a restaurant
def delete_restaurant(id):
    """

    """
    restaurant = get_restaurant(id)
    ses.delete(restaurant)
    ses.commit()


# Change a restaurant
def update_restaurant(id, restaurant_name):
    """using an id, update the details of a restaurant

    Args:
    id - (int) id from the restaurant table, for the
             restaurant being changed.
    name - (string) New Name of the restaurant.
    """
    restaurant = get_restaurant(id)
    restaurant.restaurant_name = restaurant_name
    update_item(restaurant)
