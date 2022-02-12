from typing import Optional
from fastapi import APIRouter 
from pydantic import BaseModel
import itertools
import sys
sys.path.append("..")
from depedencies import Get_Source

Api = APIRouter(
    prefix="/List_Json",
    tags=["List_Json"],
)

def Check_Data_Sync():
    if not Get_Source.Got_Data: return {"code":-1,"msg":"Data Initializing or Updating"}

class Fliter(BaseModel):
    bv:Optional[str] = None
    liveroom:Optional[str] = None
    title:Optional[str] = None
    staff:Optional[list] = None
    scene:Optional[list] = None
    skin:Optional[list] = None
    types:Optional[list] = None
    keywords:Optional[str] = None
    reverse:Optional[int] = 0

########################### Apis ###########################
@Api.post("/V1/Main_Fliter")
@Get_Source.Statistics
def Fliter_Main(fliter:Fliter):
    if Check_Data_Sync() != None: return Check_Data_Sync()
    fliter_dict = fliter.dict()
    final_dict = []

    def do_append(item):
        final_dict.count(item) == 0 and final_dict.append(item)
    def list_compare(ListA,ListB):
        add = False
        for a,b in itertools.product(ListA,ListB): 
            if a == b: add = True
        return add

    if fliter_dict["bv"] != None: return Return_Main_Data(bv=fliter_dict["bv"])

    for item in Get_Source.Main_Json:
        if (fliter_dict["liveroom"] != None) and (fliter_dict["liveroom"] != item["liveRoom"]): continue
        if (fliter_dict["title"] != None) and (fliter_dict["title"] not in item["title"]): continue
        
        # Purify_Skin
        Item_Skin = []
        for _,fn in item["skin"].items():
            Item_Skin+= fn
        stfs = {"staff":item["staff"],"scene":item["scene"],"types":item["type"],"skin":Item_Skin}
        add = True
        for _k,_v in stfs.items():
            if fliter_dict[_k] != None: add = list_compare(fliter_dict[_k],_v)

        Key_Word_Check = False
        if fliter_dict["keywords"] != None:
            if (fliter_dict["keywords"] in item["title"]) or (fliter_dict["keywords"] in ''.join(item["tags"])): Key_Word_Check = True
            for i in item["items"]:
                if fliter_dict["keywords"] in i["item"]: Key_Word_Check = True
        else: Key_Word_Check = True
        if add and Key_Word_Check: do_append(item)

    return {"code":0,"msg":"ok","data":fliter_dict["reverse"] and final_dict[::-1] or final_dict}


@Api.get("/V1/Main_Data")
@Get_Source.Statistics
def Return_Main_Data(bv:str="",reverse:int=0):
    if Check_Data_Sync() != None: return Check_Data_Sync()
    if len(bv) ==0 :return {"code":0,"msg":"ok","data":reverse and Get_Source.Main_Json[::-1] or Get_Source.Main_Json}
    else:
        try:return {"code":0,"msg":"ok","data":Get_Source.Main_Json[Get_Source.Indexer.index(bv)]}
        except ValueError: return {"code":-1,"msg":"No Bv"}

@Api.get("/V1/Indexer_Data")
@Get_Source.Statistics
def Give_Indexer(bv:str=""):
    if Check_Data_Sync() != None: return Check_Data_Sync()
    if len(bv): 
        try:
            return {"code":0,"msg":"ok","data":Get_Source.Indexer.index(bv)}
        except ValueError:
            return {"code":-1,"msg":"No Bv"}
    else: return {"code":0,"msg":"ok","data":Get_Source.Indexer}

@Api.get("/V1/Cover_Data")
@Get_Source.Statistics
def Give_Cover(bv:str=""):
    if Check_Data_Sync() != None: return Check_Data_Sync()
    if len(bv): 
        try:
            return {"code":0,"msg":"ok","data":Get_Source.Cover[bv]}
        except KeyError:
            return {"code":-1,"msg":"No Bv"}
    else: return {"code":0,"msg":"ok","data":Get_Source.Cover}

@Api.get("/V1/Srt_Data")
@Get_Source.Statistics
def Give_Srt_Url(bv):
    if Check_Data_Sync() != None: return Check_Data_Sync()
    try:
        date = Get_Source.Main_Json[Get_Source.Indexer.index(bv)]["date"].split("-")
        clips,year,month = Get_Source.Main_Json[Get_Source.Indexer.index(bv)]["clip"] , date[0], date[1]
    except KeyError: return{"code":-1,"msg":"No Bv"}

    if clips>1 : name =  [f"{bv}-{fn+1}.srt" for fn in range(clips)] 
    else : name = [f"{bv}.srt"]

    year = "20" + year
    month  = "0" + month if int(month)==1 else month

    retuns = {"name":name,"url":[f"/db/{year}/{month}/srt/{fn}" for fn in name],"sources":Get_Source.Data_Sources}
    return {"code":0,"msg":"ok","data":retuns}

<<<<<<< HEAD:routers/List_Json.py

=======
@Api.get("/V1/Status")
@Statistics
def Give_Status():
    return {"code":0,"msg":"ok","data":{"last_update_DB":Last_Update,"Acquire_Times":Acquire_Times}}
########################################################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app:Api", host="localhost",port=5003)
>>>>>>> 17b5f5969f1411dcd363b9b26df1ac545ae76926:Main-Api/app.py
