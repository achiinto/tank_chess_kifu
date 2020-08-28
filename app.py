# app.py
from flask import Flask, request, jsonify, render_template, redirect
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
SUPPORTED_MAP_NAVI = ['NEXT', 'PREVIOUS', 'START', 'END']
game_id = 0


@app.route('/load_kifu/', methods=['GET'])
def load_kifu():
    kifu_id = request.args.get("id", None)
    current_kifu = Kifu.query.filter_by(id=kifu_id).first()
    global tank_positions
    global game_id
    game_id = kifu_id
    tank_positions = KifuLoader(current_kifu).load()
    response = {"kifu_id": kifu_id, "tank_positions": tank_positions}
    return redirect("/", code=303)

# A welcome message to test our server
@app.route('/')
def index():
    action = request.args.get("action", None) # forwrad or backward or specific step??
    global current_step
    global tank_positions
    global game_id
    if action == 'PREVIOUS':
        current_step = current_step - 1
    elif action == 'NEXT':
        current_step = current_step + 1
    elif action == 'START':
        current_step = 0
    else:
        current_step = current_step
    result = tank_positions[current_step]
    return render_template('index.html', game_id=game_id)
