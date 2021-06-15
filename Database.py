import pymongo
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["Art"]

DataCol = db["Data"]

def settings(Type, Data):
    if Type == "Change":
        print("changing these settings")
    elif Type == "Get":
        Settings =  DataCol.find({"Username" : Data["Username"]}, {"Tags":1, "Avatar":1,"Username":1,"Bio":1,"Banner":1,"AccountType":1,"AcceptingCommissions":1,"MinimumWorkTime":1,"MaxNumberOfInprogressCommissions":1,"CustomSettings":1,"Email":1,"Banking":1,"_id":0})
        Settings =list(Settings)
        print(Settings)
        Settings = Settings[0]
        return Settings
    
def commission(Type, Data):
    if Type == "Get_One":
        return "something"
    elif Type == "Get_All":
        return "something"
    elif Type == "Validate":
        return "something"
    elif Type == "Add":
        return "something"

def getData(SessionID):
    print("Unsupported Function has been called")
    return {}
def getProfile(Username):
    Profile =  DataCol.find({"Username" : Username}, {"Bio":1, "Portfolio":1,"Fee":1,"Avatar":1,"Username":1,"Tags":1,"Rank":1,"Banner":1,"_id":0})
    Profile = list(Profile)
    Profile = Profile[0]
    return Profile

def validate(Type, Data):
    Result = {}
    if Type == "Settings":
        if Data["Section"] == "Profile":
            Result["Section"] = "Profile"
            if len(Data["Bio"]) < 420:
                print(Data["Bio"])
                Result["Bio"] = Data["Bio"]
            

    return {}