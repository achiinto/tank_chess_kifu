# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
# heroku run python
# >> import os
# >> os.environ.get('DATABASE_URL')
app.secret_key = b'8JwC3yOOs9qLCC0QsJRVwWOshWguDb2B'
herokudb = 'postgres://yqngaejgysyppg:ccbfc5c3cbe205865a3421f2e45e2d711a8cf26b684a699c05ff99b01fcc4733@ec2-52-31-94-195.eu-west-1.compute.amazonaws.com:5432/d70qukt23rot06'
app.config['SQLALCHEMY_DATABASE_URI'] = herokudb
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)

from models import Kifu

admin = Admin(app, name='Kifu admin', template_mode='bootstrap3')
admin.add_view(ModelView(Kifu, db.session))



@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to Tank Chess Kifu!!</h1>"
