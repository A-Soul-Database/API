from fastapi import FastAPI
from threading import Thread
from depedencies import Get_Source
from routers import List_Json , Subtitle_Search , etc
Api = FastAPI()
Api.include_router(List_Json.Api)
Api.include_router(Subtitle_Search.app)
Api.include_router(etc.Api)

if __name__ == "__main__":
    Thread(target=Get_Source.Sync_Data).start()
    import uvicorn
    uvicorn.run(Api,host="localhost",port=5000)