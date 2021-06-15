import pymongo
from pymongo import MongoClient
import time
import re
import hashlib

Session = {}

client = MongoClient("localhost", 27017)
db = client["Art"]

DataCol = db["Data"]
UserCol = db["Users"]


def holdSession(SessionID, Username):
    Session[SessionID] = {"Username" : Username, "Age": time.time()}

def dropSession(SessionID):
    try:
        del Session[SessionID]
    except:
        print("That session never existed anyway.")

def validate(Type, InputData):
    #Checks if the username provided matches a user in the database. 
    if Type == "Username":
        Username =  DataCol.find({"Username" : InputData})
        Username = list(Username)
        if Username:
            print("True !!!!")
            return True
        else:
            print("False !!!!")
            return False
    

    #checks if the email provided exists in the database, and if it doesn't checks if it can be reached. 
    elif Type == "Email":
        EmailTest = re.match(r"[^@]+@[^@]+\.[^@]+", InputData)
        #something to handle over the net.
        if EmailTest:
            Email =  DataCol.find({"Email" : InputData})
            Email = list(Email)
            if Email:
                return True
            else:
                return False
    
    
    #checks if the username and password provided by a user match that of a user in the database.
    elif Type == "Login":
        if validate("Username", InputData["Username"]):
            #Checking the hash of the password provided matches the hash of the one we have stored for the username prpbided in the datatbvase. 
            #Password = bytes(InputData["Pwd"])
            User = list(DataCol.find({"Username" : InputData["Username"]}))
            #Hash = hashlib.scrypt(bytes(Password, encoding="utf-8"), salt=bytes(User[0]["Salt"], encoding="utf-8"),n=32,r=64,p=32,maxmem=0,dklen=128)
            print(InputData)
            if InputData["Pwd"] == User[0]["Hash"]:
                return {"Success": True}
            else:
                return {"Errors": ["Your username or password is incorrect, please try again."], "Success": False}
        else:
            return {"Errors":["Your username or password is incorrect, please try again."], "Success": False}
    

    #Checks if a session code provided is valid, and if it's older than 14 hours, the session is removed from memory.
    elif Type == "Session":
        try:
            if Session[InputData]:
                Age = time.time() - Session[InputData]["Age"]
                if Age < 50400:
                    return True
                else:
                    del Session[InputData]
                    return False
        except KeyError:
            return False
    else:
        print("Nooooo, that type of validation is not provided yet you lazy fuck.")

def getSessionUser(SessionID):
    User = Session[SessionID]
    return User

def registerUser(Username, Password, Password2, Email):
    Result = {}
    Alerts = {}
    Alerts["Errors"] = []

    #Regex that determins what passwords are valid.
    PwdCharTest = re.match("", Password)

    if Password == Password2 and len(Password) >= 8 and PwdCharTest and len(Password) <= 64:
        Result["Password"] = True
    else:
        Result["Password"] = ""
        if Password != Password2:
            Result["Password"] = Result["Password"] + " The passwords you enetered did not match."
        if len(Password) < 8:
            Result["Password"] = Result["Password"] + " Passwords must be at least 8 characters."
        if len(Password) > 64:
            Result["Password"] = Result["Password"] + " Passwords must be a maximum of 64 characters."
        if not (PwdCharTest):
            Result["Password"] = Result["Password"] + " Passwords can only contain AlphaNumeric Chraracters, and some special Characters."


    #Regex that determins what Usernames are valid 
    UsernameCharTest = re.match("^[a-zA-Z0-9_.-]+$", Username)

    if not validate("Username", Username) and len(Username) >= 1 and len(Username) <= 64 and UsernameCharTest:
        Result["Username"] = True
    else:
        Result["Username"] = ""
        if (validate("Username", Username)):
            Result["Username"] = Result["Username"] + " That username is already taken : (" + Username + ")."
        if len(Password) < 1:
            Result["Username"] = Result["Username"] + " Usernames must be at least 1 character long."
        if len(Password) > 64:
            Result["Username"] = Result["Username"] + " Usernames can't be longer than 64 characters."
        if not (UsernameCharTest):
            Result["Password"] = Result["Password"] + " Usernames can only contain AlphaNumeric Chraracters."


    #Checks if an email was provided, and if one was provided checks if it's valid. 
    if Email:
        Result["Email"] = validate("Email", Email)
        if not Result["Email"]:
            Result["Email"] = True
        else:
            Result["Email"] = False
    else:
        Result["Email"] = True


    # Checks for any errors that took place in the past 20 million if statements, if none took place it does nothing, if errors happened, they are all collected. 
    print(Result)
    for x in Result: 
        if Result[x] == True:
            print(Result[x])
        else:
            Alerts["Errors"].append(Result[x])
    if Alerts["Errors"]:
        print("Errors exist")
    else:
        del Alerts["Errors"]

    print("Checking for aletrs")
    if bool(Alerts):
        Alerts["Success"] = False
    else:
        Alerts["Success"] = True
    print(Alerts)

    print("Checking if aletrs are true")
    #If everything went okay, we send a request to our data base to add the new user. 
    if(Alerts["Success"]):
        Hash = Password
        NewUser = {"Username": Username, "Hash": Hash, "Email": Email, "Created": time.time()}
        DataCol.insert_one(NewUser)
        print("Attempted to add " + Username + "to datatbase")
        if Email:
            validate("SendEmail", Email)
    else:
        print("Alerts are lies")
    return Alerts

def YourMum():
    return "something"