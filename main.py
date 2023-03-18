import pyrebase
import logging
import sys
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import render_template
from flask import make_response
import pdfkit
import random

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
person = {"is_logged_in": False, "name": "", "email": "", "uid": "", "vsub": "", "vsubname": ""}
person1 = {"is_logged_in": False, "name": "", "email": "", "uid": "", "vsub": "", "vsubname" : ""}
person2 = {"is_logged_in": False, "name": "", "email": "", "uid": "", "vsub": "", "vsubname" : ""}

config1 = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

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
            auth.create_user_with_email_and_password(validator_email, validator_password)
            global person1
            # person1["is_logged_in"] = True
            person1["email"] = validator_email
            person1["uid"] = random.randint(1,100000000)
            person1["name"] = validator_name
            person1["vsub"] = subject_code
            person["vsubname"] = subject_name
            #Append data to the firebase realtime database
            data = {"validator name": validator_name, "validator email": validator_email, "validator password": validator_password, "validator subject":subject_code, "validator subject name":subject_name}
            # if(name=="admin" and email=="admin@qgen.com"):   #password = admin@qgen
            db.child("validators").child(person1["uid"]).set(data)
            # db.child("validators").child(str(len(val_list_1.val()))).set(validator_details)
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
    
@app.route("/downproc", methods=["POST","GET"])
def downproc():
    if person["is_logged_in"] == True:
        if request.method == "POST":
            res1 = list(request.form.listvalues())
            res2=[]
            for i in res1:
                res2.extend(i)
            print(res2)
        name = "Sharwin Xavier R"
        html = render_template(
            "certificate.html",
            name=name)
        pdf = pdfkit.from_string(html, configuration=config1)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        return response
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
            elif(person["email"][:3]=="val"):
                data = db.child("users").get()
                person["name"] = data.val()[person["uid"]]["name"]
                return redirect(url_for('vallist'))
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
                lid = list(valdata.val().items())[0][0]
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
                    print("blah")
                    # page = auth.list_users()
                    # while page:
                    #     for user in page.users:
                    #         print('User: ' + user.uid)
                    #     # Get next batch of users.
                    #     page = page.get_next_page()

                    # # Iterate through all users. This will still retrieve users in batches,
                    # # buffering no more than 1000 users in memory at a time.
                    # for user in auth.list_users().iterate_all():
                    #     print('User: ' + user.uid)
                    user1 = auth.sign_in_with_email_and_password(email, password)
                    print("blah1")
                    global person2
                    person2["is_logged_in"] = True
                    person2["email"] = user1["email"]
                    person2["uid"] = lid
                    person2["name"] = name
                    person2["vsub"] = temp
                    person2["vsubname"] = temp1
                    print("blah2")
                    return redirect(url_for('vallist'))
                    # return render_template("vallist.html", email=email, password=password, validator_subject = temp, validator_subject_name=temp1, uid1=lid)
                    # return render_template("vallist.html")
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
        
@app.route("/vallist")
def vallist():
    if person2["is_logged_in"] == True:
        return render_template("vallist.html", email = person2["email"], name = person2["name"], validator_subject = person2["vsub"], validator_subject_name = person2["vsubname"])
        # return render_template("vallist.html", email = "blah!")
        # return 'hi'
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
            # person["vsub"] = ""
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            
            # if(name=="admin" and email=="admin@qgen.com"):   #password = admin@qgen
            db.child("users").child(person["uid"]).set(data)
            
            if(email[:3]=='val'):
                
                # print(vsub,vsubname,person["email"])
                valdata = {"validator name": name, "validator email": email, "validator subject": "ahh", "validator subject name": ""}
                db.child("validators").child(person["uid"]).set(valdata)
                lido = db.child("validators").child(person["uid"]).get()
                vsub = list(lido.val().items())[2][1]
                vsubname = list(lido.val().items())[3][1]
                person["vsub"] = vsub
                person["vsubname"] = vsubname
                return redirect(url_for('vallist'))
            else:
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
