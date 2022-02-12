from fastapi import APIRouter
import sys
sys.path.append("..")
from depedencies import Get_Source

Api = APIRouter(
    prefix="/Info",
    tags=["Info"],
)

@Api.get("/V1/Status")
@Get_Source.Statistics
def Give_Status():
    return {"code":0,"msg":"ok","data":{"last_update_DB":Get_Source.Last_Update,"Acquire_Times":Get_Source.Acquire_Times}}