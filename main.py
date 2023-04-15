import pyrebase
import logging
import sys
import flask
from flask import Flask, flash, redirect, render_template, request, jsonify, session, abort, url_for
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
            ress1 = list(request.form.listvalues())
            ress2=[]
            for i in ress1:
                ress2.extend(i)
            print(ress2)
        # return 'hi'
        return render_template("downroc1.html", email=person["email"], name = person["name"], specs=ress2)
    else:
        return redirect(url_for('login'))
    

@app.route("/tempdownproc", methods=["POST","GET"])
def tempdownproc():
    if person["is_logged_in"] == True:
        if request.method == "POST":
            res1 = list(request.form.listvalues())
            res2=[]
            for i in res1:
                res2.extend(i)
            print(res2)
        specis = res2[0:3]
        print(specis)
        que_specis=res2[3:3+int(res2[2])*3]
        print(que_specis)
        res2=res2[len(specis)+len(que_specis):]
        print(res2)
        # flag=0
        section_requirements = [[] for i in range(int(specis[2]))]
        j=0
        k=0
        for i in range(0,len(que_specis),3):
            print(que_specis[i])
            temp = int(que_specis[i])
            marks = int(que_specis[i+1])//int(que_specis[i])
            while(temp):
                section_requirements[k].append(res2[j])
                j=j+1
                section_requirements[k].append(res2[j])
                j=j+1
                section_requirements[k].append(marks)
                # j=j+1
                temp=temp-1
            k=k+1
        
        print(section_requirements)
        temp1=[]
        tempdict = {}
        for i in range(0,len(section_requirements)):
            for j in range(0,len(section_requirements[i]),3):
                if(j==0):
                    reto = db.child("questions").child(specis[0]).order_by_child("co_level").equal_to(section_requirements[i][j]).get()
                    reto_det = list(reto.val().items())
                    for k in range(len(reto_det)):
                        if(int(reto_det[k][1]["mark"])==section_requirements[i][j+2] and reto_det[k][1]["difflev"]==section_requirements[i][j+1]):
                            print("yes")
                            if(reto_det[k][1]["img_url"]):
                                temp1.append(reto_det[k][1]["question"] + '|' + reto_det[k][1]["img_url"])
                            else:
                                temp1.append(reto_det[k][1]["question"])
                            print(temp1)
                            break
                else:
                    reto1 = db.child("questions").child(specis[0]).order_by_child("co_level").equal_to(section_requirements[i][j]).get()
                    reto1_det = list(reto1.val().items())
                    # print(len(reto1_det))
                    for l in range(len(reto1_det)):
                        if(int(reto1_det[l][1]["mark"])==section_requirements[i][j+2] and reto1_det[l][1]["difflev"]==section_requirements[i][j+1]):
                            thres_ret = threshold(temp1,reto1_det[l][1]["question"])
                            if(reto1_det[l][1]["img_url"]):
                                tempdict.update({reto1_det[l][1]["question"] + '|' + reto1_det[l][1]["img_url"]:thres_ret})
                            else:
                                tempdict.update({reto1_det[l][1]["question"]:thres_ret})
                    sorted_tempdict = sorted(tempdict)
                    print("hi")
                    print(tempdict)
                    print(sorted_tempdict)
                    # temp1.append(str(next(iter(sorted_tempdict))))
                    temp1.append(sorted_tempdict[0])
                    print(temp1)
                    tempdict = {}
                    sorted_tempdict={}
        print(temp1)
       
        # return 'hi'
        return render_template("pdftemp.html",questions = temp1,specis1 = specis, que_specis1=que_specis,section_requirements1=section_requirements,lenspec = specis[2])
    else:
        return redirect(url_for('login'))
    
def threshold(temp,question):
        synmatch = 0
        # match_percent = 0
        que_spl = question.split()
        for m in range(len(temp)):
            temp_spl = temp[m].split()
            if(len(que_spl)>len(temp_spl)):
                long = que_spl
                short = temp_spl
            else:
                long = temp_spl
                short = que_spl
            for n in short:
                for o in long:
                    if(n==o):
                        synmatch += (1/len(short))*100
        return synmatch

@app.route("/output",methods=["POST", "GET"])
def output():
    if person["is_logged_in"]==True:
        if request.method=="POST":
            jes = list(request.form.listvalues())
            jes2=[]
            for i in jes:
                jes2.extend(i)
            print(jes2)
        specis = jes2[0:3]
        print(specis)
        que_specis=jes2[3:3+int(jes2[2])*3]
        print(que_specis)
        jes2=jes2[len(specis)+len(que_specis):]
        # print(jes2)
        total_questions=0
        for x in range(0,len(que_specis),3):
            total_questions += int(que_specis[x])
        section_requirements = [[] for i in range(int(specis[2]))]
        j=0
        k=0
        for i in range(0,len(que_specis),3):
            temp = int(que_specis[i])
            while(temp):
                section_requirements[k].append(jes2[j])
                j=j+1
                section_requirements[k].append(jes2[j])
                j=j+1
                section_requirements[k].append(jes2[j])
                j=j+1
                temp=temp-1
            k=k+1
        print(section_requirements)
        jes2=jes2[total_questions*3:]
        questions = [[] for i in range(int(specis[2]))]
        l=0
        m=0
        for i in range(0,len(que_specis),3):
            temp1 = int(que_specis[i])
            while(temp1):
                questions[m].append(jes2[l])
                l=l+1
                temp1=temp1-1
            m=m+1
        print(questions)
        jes2=jes2[total_questions+1:]
        elements = jes2
        print(elements)
        html = render_template(
            "certificate.html",
            elements=elements,questions=questions,specis=specis,que_specis=que_specis,section_requirements=section_requirements)
        pdf = pdfkit.from_string(html, configuration=config1)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        return response
        return 

@app.route("/downproc", methods=["POST","GET"])
def downproc():
    if(person["is_logged_in"]==True):
        return "hi"
    
@app.route("/uptemp",methods=["POST","GET"])
def uptemp():
    if(person["is_logged_in"]==True):
        if request.method == "POST":
            res1 = list(request.form.listvalues())
            print(res1)
            res2=[]
            for i in res1:
                res2.extend(i)
            print(res2)
            return render_template("uptemp.html",specs=res2)
        else:
            return redirect(url_for('welcome'))
    return 'hi'

@app.route("/uproc", methods=["POST","GET"])
def uproc():
    if request.method == "POST":
        res1 = list(request.form.listvalues())
        print(res1)
        res2=[]
        for i in res1:
            res2.extend(i)
        a=res2.pop(0)
        print(res2)
        print(a)
        syll = db.child("subjects").order_by_child("subject code").equal_to(a).get()
        # print(list(syll.val().items())[0][1])
        tes1 = syll.val().items()
        print(tes1)
        tes2=[]
        for l in tes1:
            tes2.extend(l)
        print(tes2[1]["syllabus"])
        
        # print(list(syll.val().items())[0])
        # syllspl = list(syll.val().items()).split()
        syllspl = tes2[1]["syllabus"].split()
        
        try:
            for i in range(0,len(res2),6):
                match_percentage = 0
                global question
                question_details = {"question":res2[i],"mark":res2[i+1],"difflev":res2[i+2],"co_level":res2[i+3],"ko_level":res2[i+4],"img_url":res2[i+5]}
                temp = db.child("questions").child(a).get()
                print(temp.val())
                temp2 = db.child("pending_questions").child(a).get()
                splque = res2[i].split()
                lensplque = len(splque)
                for j in splque:
                    for k in syllspl:
                        if(j==k):
                            match_percentage += (1/lensplque)*100
                            break
                print(match_percentage)
                if(match_percentage>=20):
                    if(temp.val() is not None):
                        db.child("questions").child(a).child(str(len(temp.val()))).set(question_details)
                    else:
                        db.child("questions").child(a).child("0").set(question_details)
                else:
                    if(temp2.val() is not None):
                        db.child("pending_questions").child(a).child(str(len(temp2.val()))).set(question_details)
                    else:
                        db.child("pending_questions").child(a).child("0").set(question_details)
                    # temp2 = db.child("validators").order_by_child("validator subject").equal_to(a).get()
                    # print(temp2.val())
                    # if(temp2.val() is not None):

                    #     db.child("validators").order_by_child("validator subject").equal_to(a).child("pending").child(str(len(temp2.val()))).set(question_details)
                    # else:
                    #     db.child("validators").order_by_child("validator subject").equal_to(a).child("pending").child("0").set(question_details)
            return 'Uploaded successfully'
        except:
            return 'failed'
        

# @app.route('/valdec', methods=["POST", "GET"])
# def valdec():
#   if request.method == 'POST':
#     data = request.get_json()
#     query = data['query']
#     print(query)
#     # layout = flask.request.args.get('layout')
#     # print(layout)
# #   return Flask.jsonify({'html':Flask.render_template('station.html',target=layout)})
#     return 'hibbo'
#   else:
#       return "hobbo"


@app.route('/api/questions/<subjectcode>/<question>/accept', methods=['POST'])
def accept_question(subjectcode, question):
    print(subjectcode,question)
    valpro = db.child('pending_questions').child(subjectcode).order_by_child("question").equal_to(question).get()
    
    # db.child("subjects").child(str(len(sub_list_1.val()))).set(subject_details)
    stemp = db.child("questions").child(subjectcode).get()
    que_det = list(valpro.val().items())[0][1]
    # if(len(stemp.val())==0):
    #     db.child("questions").child(subjectcode).child("0").set(que_det)
    # else:
    db.child("questions").child(subjectcode).child(str(len(stemp.val()))).set(que_det)
    db.child("pending_questions").child(subjectcode).child(list(valpro.val().items())[0][0]).remove()
    return jsonify({'success': True})
    

@app.route('/api/questions/<subjectcode>/<question>/reject', methods=['DELETE'])
def reject_question(subjectcode,question):
    valpro1 = db.child('pending_questions').child(subjectcode).order_by_child("question").equal_to(question).get()
    db.child("pending_questions").child(subjectcode).child(list(valpro1.val().items())[0][0]).remove()
    return jsonify({'success': True})

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
                    user1 = auth.sign_in_with_email_and_password(email, password)
                    print("blah1")
                    global person2
                    person2["is_logged_in"] = True
                    person2["email"] = user1["email"]
                    person2["uid"] = lid
                    person2["name"] = name
                    person2["vsub"] = temp
                    person2["vsubname"] = temp1
                    # person2["pending"] 
                    print("blah2")
                    return redirect(url_for('vallist'))
               
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
        pen_det = db.child("pending_questions").child(person2["vsub"]).get()
        temproc = pen_det.val()
        # fes = len(temproc)
        if temproc is None:
            fes=0
        else:
            fes = len(temproc)
        
        return render_template("vallist.html", email = person2["email"], name = person2["name"], validator_subject = person2["vsub"], validator_subject_name = person2["vsubname"], specs1 = temproc, len1 = fes)
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
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))
        
@app.template_filter('ascii_to_char')
def ascii_to_char(value):
    return chr(int(value))

if __name__ == "__main__":
    app.run(debug=True)
