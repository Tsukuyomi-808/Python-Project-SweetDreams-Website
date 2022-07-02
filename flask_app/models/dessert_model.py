from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash,session
from flask_app.models.client_model import Client

class Dessert: 
  def __init__(self,data):
    self.data = data['id']
    self.flavor = data['flavor']
    self.description = data['description']
    self.instructions = data['instructions']
    self.dairy = data['dairy']
    self.gluten = data['gluten']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']


  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM desserts LEFT JOIN orders ON desserts.id = orders.dessert_id JOIN clients ON clients.id = orders.client_id WHERE desserts.id = %(id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    dessert = cls(results[0])
    for row in results:
      if row['clients.id'] == None:
        break
      data = {
        "id": row['clients.id'],
        "first_name": row['first_name'],
        "last_name" : row['last_name'],
        "email": row['email'],
        "password": row['password'],
        "created_at": row['created_at'],
        "updated_at": row['updated_at']
      }
      dessert.clients_who_ordered.append(Client.client(data))
    return dessert
