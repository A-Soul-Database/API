from fastapi import FastAPI
from threading import Thread
from depedencies import Get_Source
from routers import List_Json , Subtitle_Search , etc
Api = FastAPI(
        docs_url="/Api/docs",
        openapi_url="/Api/openapi"
        )
Api.include_router(List_Json.Api,prefix="/Api")
Api.include_router(Subtitle_Search.app,prefix="/Api")
Api.include_router(etc.Api,prefix="/Api")

if __name__ == "__main__":
    Thread(target=Get_Source.Sync_Data).start()
    import uvicorn
    uvicorn.run(Api,host="localhost",port=5000)
