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
from services.kifu import KifuLoader

admin = Admin(app, name='Kifu admin', template_mode='bootstrap3')
admin.add_view(ModelView(Kifu, db.session))


# As single cache layer
current_kifu = None
current_step = 0
tank_positions = [{}]

@app.route('/load_kifu/', methods=['GET'])
def load_kifu():
    kifu_id = request.args.get("id", None)
    current_kifu = Kifu.query.filter_by(id=kifu_id).first()
    tank_positions = KifuLoader(current_kifu).load()
    # call a service to create the setup of board and pieces
    # Set the cache with these.
    response = {"kifu_id": kifu_id, "tank_positions": tank_positions}
    return jsonify(response)

# A welcome message to test our server
@app.route('/')
def index():
    action = request.args.get("action", None) # forwrad or backward or specific step??
    # call a service to create the setup of board and pieces at the specific stage. using the cache
    # set the cache with these
    # let the page to render the board and tank. given the object.
    return "<h1>Welcome to Tank Chess Kifu!!</h1>"
