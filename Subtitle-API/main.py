from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from config import configs
import json

class SearchPara(BaseModel):
    words: str

class SearchRes(BaseModel):
    key: int
    bv:str
    date:str
    hour:str
    title:str
origins = [
    "*"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def match(subtitles: str, search_words: str):
    return search_words.lower() in subtitles.lower()

@app.post("/sub_search",response_model=List[SearchRes])
async def search(para: SearchPara):
    data_path = configs['data_path'] # path to A-Soul-Data
    words = para.words
    
    with open(data_path+'/db/main.json') as f:
        years = json.load(f)['LiveClip']
    main_json = []
    search_json = {}
    for year in years:
        mj_path = data_path+'/db/'+year+'/main.json'
        search_path = data_path+'/db/'+year+'/search.json'
        with open(mj_path) as f:
            main_json += json.load(f)
        with open(search_path) as f:
            search_json.update(json.load(f))
    table_list = []
    for k, data in enumerate(main_json):
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
            subtitles = search_json[bv]['srt']
        except:
            continue
        if match(subtitles,words):
            search_res.append(data)
    return search_res

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=configs['port'])