from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html',restaurants=restaurants)



@app.route('/restaurant/new',methods=['GET', 'POST'])
def newRestaurant():
    if(request.method=='POST'):
        restaurant=Restaurant(name=request.form['name'])
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit',methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if(request.method=='POST'):
        restaurant.name=request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html',restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete',methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if(request.method=='POST'):
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html',restaurant=restaurantToDelete)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant=restaurant,items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new',methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if(request.method=='POST'):
        menuItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id,description=request.form['description'],price=request.form['price'],course=request.form['course'])
        session.add(menuItem)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:    
        return render_template('newMenuItem.html',restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=['GET', 'POST'])
def editMenuItem(restaurant_id,menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if(request.method=='POST'):
        editedItem.name=request.form['name']
        editedItem.description=request.form['description']
        editedItem.price=request.form['price']
        editedItem.course=request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html',item=editedItem,restaurant_id=restaurant_id,menu_id=menu_id)



@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id,menu_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if(request.method=='POST'):
        session.delete(item)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',restaurant=restaurant,item=item)

    

@app.route('/restaurants/JSON')
def showRestaurantsJson():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def showMenuItemsJson(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showSpecificMenuItemJson(restaurant_id,menu_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(id=menu_id).one()
    return jsonify(MenuItems=[item.serialize])



if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5003)



