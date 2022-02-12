from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import sys
sys.path.append("..")
from depedencies import Get_Source

app = APIRouter(
    prefix="/Subtitle_Search",
    tags=["Subtitle_Search"],
)

class SearchPara(BaseModel):
    words: str

class SearchRes(BaseModel):
    key: int
    bv:str
    date:str
    hour:str
    title:str

def match(subtitles: str, search_words: str):
    return search_words.lower() in subtitles.lower()

@app.post("/sub_search",response_model=List[SearchRes])
async def search(para: SearchPara):
    words = para.words
    table_list = []
    for k, data in enumerate(Get_Source.Main_Json):
        try:
            title = data['title']
            bv = data['bv']
            date = data['date']
            hour = data['time']
        except:
            print("Error when parse main_json! k:"+str(k))
            print(data)
        table_list.append({
            'key':k,
            'date':date,
            'hour':hour,
            'bv':bv,
            'title':title
        })
    table_list.reverse()
    search_res = []
    for data in table_list:
        bv = data['bv']
        try:
            subtitles = Get_Source.Search_Json[bv]['srt']
        except:
            continue
        if match(subtitles,words):
            search_res.append(data)
    return {"code":0,"msg":"ok","data":search_res}
