from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CarMake, CarModel

from functools import wraps
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "UdacityFullStackProject"

# Connect to Database and create database session
engine = create_engine('sqlite:///carlist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def x(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return x


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
	# Render the Login Template
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 50px; height: 50px;\
        border-radius: 150px;-webkit-border-radius: 150px;\
        -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
             'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('Successfully disconnected.')
        carMakes = session.query(CarMake).all()
        # return "This page will show all car makes"
        return render_template('makes.html', carMakes=carMakes)
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/make/<int:carmake_id>/model/JSON')
def makeListJSON(carmake_id):
    makes = session.query(CarMake).filter_by(id=carmake_id).one()
    models = session.query(CarModel).filter_by(
        carmake_id=carmake_id).all()
    return jsonify(Models=[m.serialize for m in models])


@app.route('/make/<int:carmake_id>/model/<int:model_id>/JSON')
def modelItemJSON(carmake_id, model_id):
    models = session.query(CarModel).filter_by(id=model_id).one()
    return jsonify(models=models.serialize)


@app.route('/make/JSON')
def makesJSON():
    makes = session.query(CarMake).all()
    return jsonify(makes=[m.serialize for m in makes])


# Show all Makes
@app.route('/')
@app.route('/make/')
def showMakes():
    carMakes = session.query(CarMake).all()
    # return "This page will show all car makes"
    return render_template('makes.html', carMakes=carMakes)


# Create a new make
@app.route('/make/new/', methods=['GET', 'POST'])
@login_required
def newMake():
    if request.method == 'POST':
        newMake = CarMake(name=request.form['name'],
                          creator=login_session['email'])
        session.add(newMake)
        session.commit()
        flash("Car Make Successfully Added!")
        return redirect(url_for('showMakes'))
    else:
        return render_template('newMake.html')


# Edit a make
@app.route('/make/<int:carmake_id>/edit/', methods=['GET', 'POST'])
@login_required
def editMake(carmake_id):
    editedMake = session.query(
        CarMake).filter_by(id=carmake_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedMake.name = request.form['name']
            flash("Car Make Successfully Edited!")
            return redirect(url_for('showMakes'))
    else:
        return render_template(
            'editMake.html', carmake=editedMake)


# Delete a make
@app.route('/make/<int:carmake_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteMake(carmake_id):
    makeToDelete = session.query(
        CarMake).filter_by(id=carmake_id).one()
    if request.method == 'POST':
        session.delete(makeToDelete)
        session.commit()
        flash("Car Make Deleted!")
        return redirect(
            url_for('showMakes', carmake_id=carmake_id))
    else:
        return render_template(
            'deleteMake.html', carmake=makeToDelete)


# Show a make's models
@app.route('/make/<int:carmake_id>/')
@app.route('/make/<int:carmake_id>/model/')
def showModel(carmake_id):
    make = session.query(CarMake).filter_by(id=carmake_id).one()
    models = session.query(CarModel).filter_by(
        carmake_id=carmake_id).all()
    return render_template('model.html', models=models, make=make)


# Create a new car model
@app.route(
    '/make/<int:carmake_id>/model/new/', methods=['GET', 'POST'])
@login_required
def newCarModel(carmake_id):
    if request.method == 'POST':
        newModel = CarModel(name=request.form['name'], url=request.form[
                           'url'], msrp=request.form['msrp'],
                           carType=request.form['carType'],
                           carmake_id=carmake_id)
        session.add(newModel)
        session.commit()
        flash("New Car Model Added!")
        return redirect(url_for('showModel', carmake_id=carmake_id))
    else:
        return render_template('newModel.html', carmake_id=carmake_id)

    return render_template('newModel.html', make=make)


# Edit a car model
@app.route('/make/<int:carmake_id>/model/<int:model_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editCarModel(carmake_id, model_id):
    editedModel = session.query(CarModel).filter_by(id=model_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedModel.name = request.form['name']
        if request.form['url']:
            editedModel.url = request.form['url']
        if request.form['msrp']:
            editedModel.msrp = request.form['msrp']
        if request.form['carType']:
            editedModel.carType = request.form['carType']
        session.add(editedModel)
        session.commit()
        flash("Car Model Successfully Edited!")
        return redirect(url_for('showModel', carmake_id=carmake_id))
    else:

        return render_template(
            'editCarModel.html', carmake_id=carmake_id,
            model_id=model_id, carmake=editedModel)


# Delete a car model
@app.route('/make/<int:carmake_id>/model/<int:model_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteCarModel(carmake_id, model_id):
    modelToDelete = session.query(CarModel).filter_by(id=model_id).one()
    if request.method == 'POST':
        session.delete(modelToDelete)
        session.commit()
        flash("Car Model Deleted!")
        return redirect(url_for('showModel', carmake_id=carmake_id))
    else:
        return render_template('deleteCarModel.html',
                               model=modelToDelete, carmake_id=carmake_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
