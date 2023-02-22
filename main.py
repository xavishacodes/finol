import pyrebase
import logging
import sys
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {
  "apiKey": "AIzaSyD1cQdqd0JFGIu6kxF8Pl7uf9GSf_AMytk",
  "authDomain": "finol-752a9.firebaseapp.com",
  "databaseURL": "https://finol-752a9-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "finol-752a9.appspot.com"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/vsignin")
def vsignin():
    return render_template("vsignin.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

@app.route("/dashboard")
def dashboard():
    if person["is_logged_in"] == True:
        sub_list = db.child('subjects').get()
        print(sub_list.val())
        return render_template("dashboard.html", email=person["email"],name =person["name"], places=sub_list.val())

    else:
        return redirect(url_for('login'))

@app.route("/add")
def add():
    if person["is_logged_in"] == True:
        if person["name"] =="admin1":
            return render_template("add.html", email = person["email"], name=person["name"])
    else:
        return redirect(url_for('login'))

@app.route("/newsub",  methods = ["POST", "GET"])
def newsub():
    if request.method == "POST":
        res1 = request.form 
        subject_name=res1["subject_name"]
        subject_code=res1["subject_code"]
        syllabus=res1["syllabus"]
        validator_email=res1["valem"]
        validator_name=res1["valname"]
        validator_password=res1["valpass"]
        try:
            global subject 
            subject_details = {"subject name": subject_name, "subject code": subject_code, "syllabus": syllabus, "validator name": validator_name, "validator password": validator_password, "validator email": validator_email}
            sub_list_1 = db.child('subjects').get()
            db.child("subjects").child(str(len(sub_list_1.val()))).set(subject_details)
            validator_details = {"validator email": validator_email, "validator password": validator_password, "validator name": validator_name, "validator subject": subject_code, "validator subject name": subject_name}
            val_list_1 = db.child('validators').get()
            db.child("validators").child(str(len(val_list_1.val()))).set(validator_details)
            return redirect(url_for('dashboard'))
        except:
            return redirect(url_for('login'))

@app.route("/upload")
def upload():
    if person["is_logged_in"] == True:

        temp = db.child("subjects").get()

        temp1=[]
        for val in temp.val():
                    for k, v in val.items():
                        if k=='subject code':
                            temp1.append(v)
        print(temp1)
        return render_template("upload.html", email = person["email"], name = person["name"], subject_list=temp1)
    else:
        return redirect(url_for('login'))

@app.route("/download")
def download():
    if person["is_logged_in"] == True:

        temp = db.child("subjects").get()

        temp1=[]
        for val in temp.val():
                    for k, v in val.items():
                        if k=='subject code':
                            temp1.append(v)
        print(temp1)
        return render_template("download.html", email = person["email"], name = person["name"], subject_list=temp1)
    else:
        return redirect(url_for('login'))


@app.route("/downroc1", methods=["POST","GET"])
def downroc1():
    if person["is_logged_in"] == True:
        if request.method == "POST":
            res1 = list(request.form.listvalues())
            res2=[]
            for i in res1:
                res2.extend(i)
            print(res2)
        return render_template("downroc1.html", email=person["email"], name = person["name"], specs=res2)
    else:
        return redirect(url_for('login'))

@app.route("/uproc", methods=["POST","GET"])
def uproc():
    if request.method == "POST":
        res1 = list(request.form.listvalues())
        res2=[]
        for i in res1:
            res2.extend(i)
        a=res2.pop(0)
        print(res2)
        try:
            for i in range(0,len(res2),5):
                global question
                question_details = {"question":res2[i],"mark":res2[i+1],"co_level":res2[i+2],"ko_level":res2[i+3],"difflev":res2[i+4]}
                temp = db.child("questions").child(a).get()
                print(temp.val())
                if(temp.val() is not None):
                    db.child("questions").child(a).child(str(len(temp.val()))).set(question_details)
                else:
                    db.child("questions").child(a).child("0").set(question_details)
            return 'hi'
        except:
            return 'failed'

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    # print("hi")
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            # Get the name of the user
            if(person["email"]=='admin1@gmail.com'):    
                data=db.child("admin").get()
                person["name"] = data.val()[person["uid"]]["name"]
                return redirect(url_for('dashboard'))
            else:
                data = db.child("users").get()
                person["name"] = data.val()[person["uid"]]["name"]
                return redirect(url_for('welcome'))
        except:
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

@app.route("/vresult", methods = ["POST", "GET"])
def vresult():
    # print("hi")
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        print(email[:3])
        print(email[-8:])
        print(name[:9])
        try:
            if email[:3]=='val' and email[-8:]=='qgen.com' and name[:9]=='Validator':
                # print("vallllli")
                valdata = db.child("validators").order_by_child("validator name").equal_to(name).get()
                # print(valdata.val())
                flag=0
                temp=''
                temp1=''
                for val in valdata.val().values():
                    for k, v in val.items():
                        if k=='validator password':
                            if v==password:
                                flag = 1
                        if k=='validator subject':
                            temp = v
                        if k=="validator subject name":
                            temp1 = v
                # print(temp, temp1)
                # print(email, password)
                if flag==1:
                    return render_template("vallist.html", email=email, password=password, validator_subject = temp, validator_subject_name=temp1)
                # print("jojo")
                # return 'hi'
            #Try signing in the user with the given information
            # user = auth.sign_in_with_email_and_password(email, password)
            # #Insert the user data in the global person
            # global person
            # person["is_logged_in"] = True
            # person["email"] = user["email"]
            # person["uid"] = user["localId"]
            # # Get the name of the user
            # if(person["email"]=='admin1@gmail.com'):    
            #     data=db.child("admin").get()
            #     person["name"] = data.val()[person["uid"]]["name"]
            #     return redirect(url_for('dashboard'))
            # else:
            #     data = db.child("users").get()
            #     person["name"] = data.val()[person["uid"]]["name"]
            #     return redirect(url_for('welcome'))
        except:
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            # if(name=="admin" and email=="admin@qgen.com"):   #password = admin@qgen
            db.child("users").child(person["uid"]).set(data)
            return redirect(url_for('welcome'))
            # else:
            #     db.child("users").child(person["uid"]).set(data)
            # #Go to welcome page
            #     return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))
    else:
        if person["is_logged_in"] == True:
            #  if(name=="admin" and email=="admin@qgen.com"):   #password = admin@qgen
            #     return redirect(url_for('dashboard'))
            #  else:
            #Go to welcome page
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(debug=True)
