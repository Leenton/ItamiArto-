from flask import Flask, render_template, url_for, redirect, request, session, jsonify, json
import Credential
import Database
import secrets
import Log

UPLOAD_FOLDER = "./static/uploads"
app = Flask(__name__)

app.config['SECRET_KEY'] = "684a2c31fa1f159e791fbd0d0ae4214c58b1ba170543bd7085dd61c722617f9c"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def sessionCheck():
    try:
        temp = session["SessionID"]
        del temp
    except:
        session["SessionID"] = ""
def logIp():
    print(request.remote_addr)
    print(request.remote_user)

@app.route("/",  methods=["GET", "POST"])
def mainpage():
    logIp()
    #Checks if the user has a session, if they do, it redirects them to the encrypted data page, else it makes them login
    UserData = {}
    sessionCheck()
    if(session["SessionID"]):
        if(Credential.validate("Session", session["SessionID"])):
            UserData = Database.getData(Credential.getSessionUser(session["SessionID"]))
            UserData["LoggedIn"] = True
            return render_template("MainPage.html", UserData=UserData)
        else:
            UserData["LoggedIn"] = False
            return render_template("MainPage.html", UserData=UserData)
    else:
        UserData["LoggedIn"] = False
        return render_template("MainPage.html", UserData=UserData)     


@app.route("/activity",  methods=['GET', 'POST'])
def activity():
    sessionCheck()
    if(session["SessionID"]):
        if(Credential.validate("Session", session["SessionID"])):
            UserData = Database.commission("Get_All", Credential.getSessionUser(session["SessionID"]))
            return render_template("commissions.html", UserData=UserData)
        else:
            return redirect(url_for("login"))
    else:
        return render_template("login")  


@app.route("/user/<Username>",  methods=['GET', 'POST'])
def profile(Username):
    print("Profile function has been called")
    sessionCheck()
    Alerts = {}
    UserData = {}
    if request.method == "POST":
        if Credential.validate("Username", Username):
            UserData = Database.getProfile(Username)
            if Credential.validate("Session", session["SessionID"]):
                UserData["UsernameID"] = Credential.getSessionUser(session["SessionID"])["Username"]
                UserData["LoggedIn"] = True
                Data = request.form
                Data["Requester"] = Credential.getSessionUser(session["SessionID"])
                Data["ArtProvider"] = Username
                if Database.commission("Validate", Data):
                    Database.commission("Add", Data)
                    Alerts["Success"] = "Commission has been sent, check your commissions to see if they have accepted, it may take some time for the artist to get back to you due to time zones, schedules, and general life stuff. :)"
                    return render_template("profile.html", UserData=UserData, Alerts=Alerts) 
                else:
                    Alerts["Errors"] = "The form you filled out contained some errors, please try again."
                    return render_template("profile.html", UserData=UserData, Alerts=Alerts) 
            else:
                redirect(url_for("mainpage"))   
        else:
            return redirect(url_for("mainpage"))
        return redirect(url_for("mainpage"))
    else:
        if Credential.validate("Username", Username):
            UserData = Database.getProfile(Username)
            if(session["SessionID"]):
                if(Credential.validate("Session", session["SessionID"])):
                    UserData["LoggedIn"] = True
                    UserData["UsernameID"] = Credential.getSessionUser(session["SessionID"])["Username"]
                else:
                    UserData["LoggedIn"] = False
            else:
                UserData["LoggedIn"] = False
            return render_template("profile.html", UserData=UserData, Alerts=Alerts)        
        else:
            return "404, user doesn't exist buddy."
            


@app.route("/login",  methods=['GET', 'POST'])
def login():
    sessionCheck()
    if request.method == "POST":
        Result = Credential.validate("Login", request.form)
        print(request.form)
        if(Result["Success"]):
            session["SessionID"] = secrets.token_urlsafe(64)
            Credential.holdSession(session["SessionID"], request.form["Username"].lower())
            print("Successful login for user: "  + request.form["Username"])
            return redirect(url_for("mainpage"))
        else:
            return render_template("login.html", alerts=Result["Errors"])
    else:
        if(session["SessionID"]):
            if(Credential.validate("Session", session["SessionID"])):
                return redirect(url_for("mainpage"))
            else:
                return render_template("login.html")
        else:
                return render_template("login.html")  

@app.route("/logout")
def logout():
    sessionCheck()
    if session["SessionID"]:
        Credential.dropSession(["SessionID"])
        session["SessionID"] = ""
    else:
        session["SessionID"] = ""
    
    return redirect(url_for("mainpage"))
    

@app.route("/register",  methods=['GET', 'POST'])
def register():
    try:
        temp = session["SessionID"]
        del temp
    except:
        session["SessionID"] = ""

    if request.method == "POST":
        Result = Credential.registerUser(request.form["Username"], request.form["Pwd"], request.form["Pwdconf"], request.form["Email"])
        if(Result["Success"]):
            print("Account registered")
            session["SessionID"] = secrets.token_urlsafe(64)
            Credential.holdSession(session["SessionID"], request.form["Username"].lower())
            print("Successful login for user: "  + request.form["Username"])
            return redirect(url_for("mainpage"))
        else:
            return render_template("register.html", alerts=Result["Errors"])
    else:
        if(session["SessionID"]):
            if(Credential.validate("Session", session["SessionID"])):
                return redirect(url_for("mainpage"))
            else:
                return render_template("register.html")
        else:
                return render_template("register.html")

@app.route("/settings",  methods=['GET', 'POST'])
def settings():
    sessionCheck()
    Alerts = {}
    if request.method == "POST":
        if(session["SessionID"]):
            if(Credential.validate("Session", session["SessionID"])):
                Result = Database.validate("Settings", request.form)
                if Result["Success"]:
                    Database.settings("Change", Result)
            else:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))

    if(session["SessionID"]):
        if(Credential.validate("Session", session["SessionID"])):
            SettingData = Database.settings("Get", Credential.getSessionUser(session["SessionID"]))
            UserData = {}
            UserData["LoggedIn"] = True
            UserData["UsernameID"] = Credential.getSessionUser(session["SessionID"])["Username"]
            return render_template("settings.html", SettingData=SettingData, UserData=UserData, Alerts=Alerts)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route("/search",  methods=['GET', 'POST'])
def search():
    sessionCheck()
    return render_template("search.html")


@app.route("/requestdata", methods=["GET", "POST"])
def requestdata():
    sessionCheck()
    print("hello")

@app.route("/test")
def test():
    UserData = {}
    UserData["LoggedIn"] = True
    return render_template("base.html", UserData=UserData)



if __name__ == "__main__":
    app.run(use_reloader=False, host= '0.0.0.0', debug=True)