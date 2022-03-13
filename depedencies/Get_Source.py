import requests
import time
import functools

Data_Sources = ["https://livedb.asoulfan.com/db","https://raw.githubusercontent.com/A-Soul-Database/A-Soul-Data/main/db","https://cdn.jsdelivr.net/gh/A-Soul-Database/A-Soul-Data@latest/db"]
Main_Json = []
Brief_Main_Json = []
Indexer = []
Cover = {}
Search_Json = {}
Last_Update = 0
Acquire_Times = 0
Got_Data = False
def Sync_Data():
    global Main_Json, Indexer, Cover, Got_Data, Last_Update , Search_Json, Brief_Main_Json
    Db_Url = Data_Sources[1]
    while True:
        try:
            Base_Json = requests.get(Db_Url+"/main.json").json()["LiveClip"]
            main,indexer,cover,search = [],[],{},{}
            for fn in Base_Json:
                main.extend(requests.get(f"{Db_Url}/{fn}/main.json").json()),indexer.extend(requests.get(f"{Db_Url}/{fn}/indexer.json").json()),cover.update(requests.get(f"{Db_Url}/{fn}/Cover.json").json()),search.update(requests.get(f"{Db_Url}/{fn}/search.json").json())
            Got_Data = False
            Main_Json,Indexer,Cover,Search_Json, Brief_Main_Json = main,indexer,cover,search ,[{"title":i["title"],"date":i["date"],"time":i["time"],"bv":i["bv"],"type":i["type"],"staff":i["staff"]} for i in main]
            Got_Data = True
            Last_Update = time.time()
            time.sleep(60)
        except Exception as e:
            print(f"Data Sync Exception Occured : {e} \n time: {time.time()}")
            time.sleep(5)

def Statistics(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kwargs):
        global Acquire_Times
        Acquire_Times += 1
        return fn(*args,**kwargs)
    return wrapper
