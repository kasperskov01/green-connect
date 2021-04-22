# app.py
from flask import Flask, request, jsonify, render_template
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
app = Flask(__name__)
import db

# MySQL connection
app.config['MYSQL_HOST'] = 'ulsq0qqx999wqz84.chr7pe7iynqr.eu-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'g50mzk5bj9oqa059'
app.config['MYSQL_PASSWORD'] = 'zsv3r6czm0t19cg4'
app.config['MYSQL_DB'] = 'ttujoaszacnortlw'

mysql = MySQL(app)

nav = [
          {'name': 'Home', 'url': '/'},
          {'name': 'Dimmer', 'url': '/dimmer'},
          {'name': 'Meter reader', 'url': '/meter-reader'},
          {'name': 'BMS', 'url': '/bms'}
      ]

# Routes
@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'home.html',
        title="Hjem - GreenConnect",
        css_title="home",
        description="GreenConnect energy management",
        nav=nav
    )

@app.route('/dimmer')
def dimmer():
    return render_template(
        'dimmer.html',
        title="Dimmer - GreenConnect",
        css_title="dimmer",
        description="Dimming",
        nav=nav
    )

@app.route('/meter-reader')
def meter_reader():
    return render_template(
        'meter-reader.html',
        title="Meter Reader - GreenConnect",
        css_title="meter_reader",
        description="Meter Reader",
        nav=nav
    )

@app.route('/bms')
def bms():
    return render_template(
        'bms.html',
        title="BMS - GreenConnect",
        description="GreenConnect battery management system",
        nav=nav
    )


# API
@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # cursor = mysql.get_db().cursor()
    # print(cursor)

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
            "Message": f"Welcome {param} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })



@app.route('/meter-readings/post/', methods=['GET'])
def meter_readings_upload():    
    consumption = request.args.get('consumption')
    production = request.args.get('production')

    status = db.post_meter_data(mysql, consumption, production)

    return jsonify({
            "STATUS": f"{status}",
            "METHOD": "POST"
        })

@app.route('/meter-readings/', methods=['GET'])
def meter_readings():    
    meter_id = request.args.get("meter-id", None)

    data = db.get_meter_data(mysql)
    return jsonify({
        "DATA": f"{data}",
        "METHOD": "GET"
    })

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)