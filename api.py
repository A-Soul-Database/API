from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from depedencies import Get_Source
from routers import List_Json , Subtitle_Search , etc
Api = FastAPI(
        docs_url="/Api/docs",
        openapi_url="/Api/openapi"
        )
Api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)
Api.include_router(List_Json.Api,prefix="/Api")
Api.include_router(Subtitle_Search.app,prefix="/Api")
Api.include_router(etc.Api,prefix="/Api")

if __name__ == "__main__":
    Thread(target=Get_Source.Sync_Data).start()
    import uvicorn
    uvicorn.run(Api,host="localhost",port=5000)
