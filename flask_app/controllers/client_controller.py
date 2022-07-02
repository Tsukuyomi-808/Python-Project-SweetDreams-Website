########### PACKAGES #############
from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.client_model import Client
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


############ DISPLAY ####################

@app.route("/")
def display_login():
  return render_template("login.html")

@app.route("/registeration")
def display_registration():
  return render_template("/registration.html")


################################

@app.route("/client/new", methods=["POST"])
def login_client():
  data = {
    "email" : request.form [ 'email' ] #Making sure to validate the email
  }
  result = Client.get_one( data ) 
  
  if result == None:
    flash( "Wrong credentials.", "error_login")
    return redirect ("/")
  else:
    if not bcrypt.check_password_hash( result.password, request.form[ 'password'] ):
      flash( "wrong password", "error_login")
      return redirect ("/") 
    else:
      session[ 'email' ] = result.email
      session[ 'first_name' ] = result.first_name
      session[ 'last_name' ] = result.last_name
      session[ 'client_id' ] = result.id
      return redirect( "/dashboard" ) #If all conditions meet it will go to dashboard



@app.route( "/client/new", methods = ['POST'] )
def create_client():
  
  if Client.validate_register(request.form) == True:
  
    data = {
      "email" : request.form[ 'email' ]
    }
    result = Client.get_one( data )
    
    if result == None:
      # Add the new client
      data ={
        "email" : request.form['email'],
        "first_name" :request.form['first_name'],
        "last_name" :request.form['last_name'],
        "password" : bcrypt.generate_password_hash( request.form[ 'password'] )
      }
      client_id = Client.create( data )
      
      session[ 'email' ] = request.form[ 'email' ],
      session[ 'first_name' ] = request.form[ 'first_name' ],
      session[ 'last_name' ] = request.form[ 'last_name' ]
      session[ 'client_id' ] = client_id
      return redirect ( "/dashboard" )
    else:
      flash( "That email already exists, please select another one.", "error_register_email" )
      pass
  else:
    return redirect ( "/" )
