# app.py
import string
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
map_terrains = {"O2": 'b', "L2": 'b', "K2": 'b',
                "O3": 'b', "L3": 'b', "K3": 'b', "E3": 'b', "D3": 'b',
                "O4": 'b', "L4": 'b',
                "I5": 'b', "H5": 'b',
                "J6": 'b', "I6": 'b', "H6": 'b', "G6": 'b',"F6": 'b', "C6": 'b', "B6": 'b',
                "N7": 'b', "M7": 'b', "B7": 'b',
                "N8": 'b', "M8": 'b', "L8": 'b',
                "E9": 'b', "D9": 'b', "C9": 'b',
                "O10": 'b', "D10": 'b', "C10": 'b',
                "O11": 'b', "N11": 'b', "K11": 'b', "J11": 'b',"I11": 'b', "H11": 'b', "G11": 'b',
                "I12": 'b', "H12": 'b',
                "E13": 'b', "B13": 'b',
                "M14": 'b', "L14": 'b', "F14": 'b', "E14": 'b', "B14": 'b',
                "F15": 'b', "E15": 'b', "B15": 'b',
               }
tank_positions = [{}]
SUPPORTED_MAP_NAVI = ['NEXT', 'PREVIOUS', 'START', 'END']
game_id = 0
x_map_position_display = list(reversed(list(string.ascii_uppercase)[0:17]))

def position_calculator(x, y):
    # a bit reliance of the front-end
    x_alpha = x_map_position_display[x]
    return x_alpha + str(y)

class MapLayout():
    def __init__(self, map_dict):
        self.map_dict = map_dict

    def feature(self, x, y):
        map_xy = position_calculator(x, y)
        return self.map_dict.get(map_xy)

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
    global map_terrains
    global x_map_position_display

    if action == 'PREVIOUS':
        current_step = current_step - 1
    elif action == 'NEXT':
        current_step = current_step + 1
    elif action == 'START':
        current_step = 0
    else:
        current_step = current_step

    try:
        result = tank_positions[current_step]
    except:
        current_step = 0
        result = tank_positions[current_step]
    return render_template('index.html',
                           game_id=game_id,
                           step=current_step,
                           maps=MapLayout(map_terrains),
                           x_map_position_display=x_map_position_display)
