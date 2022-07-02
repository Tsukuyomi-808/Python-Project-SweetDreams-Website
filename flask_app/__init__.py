from flask import Flask

app = Flask ( __name__ )

app.secret_key = "coolproject"

DATABASE = "dessert_schema"