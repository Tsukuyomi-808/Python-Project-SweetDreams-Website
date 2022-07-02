from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Client:
  def __init__( self, data):
    self.id = data[ 'id' ]
    self.first_name = data[ 'first_name' ]
    self.last_name = data[ 'last_name' ]
    self.email = data[ 'email' ]
    self.password = data[ 'password' ]
    self.created_at = data[ 'created_at' ]
    self.updated_at = data[ 'updated_at' ]

  @classmethod
  def create ( cls, data ):
    query = "INSERT INTO clients( first_name, last_name, email, password ) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
    return  connectToMySQL( DATABASE ).query_db( query, data )

  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM clients LEFT JOIN orders ON clients.id = orders.client_id LEFT JOIN desserts ON desserts.id = orders.dessert_id WHERE clients.id = %(id)s;"
    result = connectToMySQL(DATABASE).query_db(query,data)
  


  @staticmethod
  def validate_register( data ):
    isValid = True
    
    if data['first_name'] == "error_register_first_name":
      isValid = False
      flash("Please provide your first name.", "error_register_first_name" )
    
    
    #### Flashes when there is less than 2 characters #########
    if len(data['first_name'] ) < 2:
      isValid = False
      flash( "Your Name must have at least 2 characters.", "error_register_first_name")
    
    
    if data['last_name'] == "error_register_last_name":
      isValid = False
      flash("Please provide a first name.", )
    #### Flashes when there is less than 2 characters #########
    
    
    if len(data['last_name'] ) < 2:
      isValid = False
      flash( "Your Name must have at least 2 characters.", "error_register_last_name")
    
    
    if data['email'] == "":
      isValid = False
      flash("Please provide a email.", "error_register_email" )

    if data['password'] != data['password_confirmation']:
      isValid = False
      flash("Your password do not match.", "error_register_password_confirmation" )

    if len( data[ 'password' ] ) < 8:
      flash( "Password must be at least 8 characters long.", "error_register_password" )
    
    
    if data['password_confirmation'] == "":
      isValid = False
      flash("You must provide a password confirmation.", "error_register_password" )
    
    if not EMAIL_REGEX.match( data[ 'email' ] ):
      flash( "Please provide a valid email.", "error_register_email" )
      isValid = False
    
    return isValid

  @staticmethod
  def validate_login( data ):
    isValid = True
    if data[ 'email' ] == "":
      flash( "Please provide your email.", "error_email" )
      isValid = False
    if data[ 'password' ] == "":
      flash( "Please provide your password.", "error_password" )
      isValid = False
    return isValid


  @staticmethod
  def validate_session():
    if "client_id" not in session:
      return False
    else:
      return True