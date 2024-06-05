from fastapi import HTTPException

from fastapi import APIRouter, Depends, File, UploadFile
from utils import get_input_dfs

router = APIRouter(prefix="/start")


@router.post("/load")
async def load_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    try:
        agr_df, ret_df, _ = get_input_dfs(file_bytes)
        print(agr_df)
        print(ret_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await file.close()

    # load in db logic

    return {"status": "SUCCESS"}
