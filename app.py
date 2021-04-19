# app.py
from flask import Flask, request, jsonify
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
app = Flask(__name__)
import db



app.config['MYSQL_HOST'] = 'ulsq0qqx999wqz84.chr7pe7iynqr.eu-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'g50mzk5bj9oqa059'
app.config['MYSQL_PASSWORD'] = 'zsv3r6czm0t19cg4'
app.config['MYSQL_DB'] = 'ttujoaszacnortlw'

mysql = MySQL(app)


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



@app.route('/meter-readings-upload/', methods=['POST'])
def meter_readings_upload():    
    data = db.get_meter_data(mysql)
    return jsonify({
        "DATA": f"{data}",
        "METHOD": "GET"
    })

@app.route('/meter-readings/', methods=['GET'])
def meter_readings():    
    data = db.get_meter_data(mysql)
    return jsonify({
        "DATA": f"{data}",
        "METHOD": "GET"
    })


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to the Green-Connect API!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)