from flask import Flask,session

app = Flask(__name__)
app.secret_key = b'\xc4q\xb7V\x916u<i\x8e`\x00\x80\xc7J\xd5'
DATABASE = 'recipes_schema'
