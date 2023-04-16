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
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
BG_ENV = os.environ.get('BACKGROUND') or "lime"
DBPORT = int(os.environ.get("DBPORT")) or "3306"
S3_BUCKET = os.environ.get("S3_BUCKET") or "clo835a"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
AWS_REGION = os.environ.get("AWS_REGION")
default_image = "1.jfif"



# Permission to S3 Bucket
#app.config['S3_BUCKET'] = S3_BUCKET
#app.config['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
#app.config['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
#app.config['AWS_SESSION_TOKEN'] = AWS_SESSION_TOKEN




def download_file(default_image, S3_BUCKET):
    """
    Function to download a given file from an S3 bucket
    
    """
    
    directory = "static"
    if os.path.exists(directory) and os.path.isdir(directory):
        print("Directory does not exist")
    else:
        os.makedirs(directory)
    imagepathg9 = os.path.join(directory, "1.jfif")
    print(imagepathg9)
    
  #  s3 = boto3.resource("s3",
   #         aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
   #         aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
    #        aws_session_token=app.config['AWS_SESSION_TOKEN'],
   #         region_name=AWS_REGION
   #         )
            
            
    s3 = boto3.resource("s3",
            aws_access_key_id='ASIAZHTMUDTZTYIBEYEB',
            aws_secret_access_key='df9DWJ3CPu51mGHja6bzWXfxnB5V76ryoLPNdq0w',
            aws_session_token='FwoGZXIvYXdzEEcaDOax0ZTIUllrfcEqQCLEAR2sIglm3p7lEUgi1qCYYnnKGuLRVismvu+xI+6bDKGUfmCuesho6BMmB/kKGAmSSekQg22DUjz43lSfTia8+grIkqMmWoN/HNfsSrEO8j2bESZYNoAdRHFXwNW4R3B5J/ASE+Bw2WXO6eGSE6aJAoQc7EyBy6F56WkSmeRbdYPA62IqvsxwT5uBse4FPHlWYI4tz+rceSyqDZ8333lOiSS2Oas116oqZbQHdwoIog5M8Q8052pasjYobnBkqBJ5W+rY9Hkoy+jvoQYyLa/MPkK3GL3x2N2BYSxJVPtPxeSfw8+HrwOzFlu1UAdUcicTo3GPYPr3azztLg=='
            )        
            
    print({S3_BUCKET})
    s3.Bucket(S3_BUCKET).download_file("1.jfif", imagepathg9)
    return imagepathg9



#object = S3_BUCKET.Object('1.jfif')
#image = tempfile.NamedTemporaryFile()

            
            

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
COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink", "lime"])



    
    
    
    

#Code to download file

#def download_file(bg, bucket):
 #   s3 = boto3.resource('s3')
  #  output = f"/media/bg.jpg"
   #return output

#SUPPORTED_BG = ",".join(bg_url.keys())

#BG = random.choice(["bg1", "bg2"])


#def imageSource(bucket, object, image):
#    with open(image.name, 'wb') as f:
#    object.download_fileobj(f)
#    src = image.name    #dir/subdir/2015/12/7/img01.jpg
#    return src







@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', background=background)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('addemp.html', background=background)
    
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
    return render_template('addemp.html', background=background)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
     return render_template("getemp.html", background=background)


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
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], background=background)

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
