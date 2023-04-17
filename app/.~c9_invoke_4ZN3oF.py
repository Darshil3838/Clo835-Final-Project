from flask import Flask, render_template, request
import flask
from pymysql import connections
import os
import random
import argparse
import boto3


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "pw"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
DBPORT = int(os.environ.get("DBPORT")) or "3306"
S3_BUCKET = os.environ.get("S3_BUCKET") or "finalg9s3"
BG_ENV = os.environ.get('BACKGROUND') or "blue"
GROUP_NAME = os.environ.get('GROUP_NAME') or "Group9"
AWS_REGION = os.environ.get("AWS_REGION")
default_image = os.environ.get("default_image") or "g901.jpg"



def download_file(default_image, S3_BUCKET):

    
    directory = "static"
    if os.path.exists(directory) and os.path.isdir(directory):
        print("Directory does not exist")
    else:
        os.makedirs(directory)
    imagepathg9 = os.path.join(directory, default_image)
    print(imagepathg9)
    s3 = boto3.resource("s3",)        
            
    print({S3_BUCKET})
    s3.Bucket(S3_BUCKET).download_file(default_image, imagepathg9)
    return imagepathg9

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';

# Define the supported color codes
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}


# Create a string of supported colors
SUPPORTED_COLORS = ",".join(color_codes.keys())

# Generate a random color
#COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink", "lime"])


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', background=background, GROUP_NAME=GROUP_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('addemp.html', background=background, GROUP_NAME=GROUP_NAME )
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addemp.html', background=background, GROUP_NAME=GROUP_NAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
     return render_template("getemp.html", background=background, GROUP_NAME=GROUP_NAME)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], background=background, GROUP_NAME=GROUP_NAME )

if __name__ == '__main__':
    background=download_file(default_image, S3_BUCKET)
    print(background)
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if BG_ENV:
            print("A color was set through environment variable -" + BG_ENV + ". However, color from command line argument takes precendence.")
    elif BG_ENV:
        print("No Command line argument. Color from environment variable =" + BG_ENV)
        COLOR = BG_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

    # Check if input color is a supported one
    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    app.run(host='0.0.0.0',port=81,debug=True)
