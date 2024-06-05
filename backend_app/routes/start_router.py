from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, UploadFile
from utils import get_input_dfs
from db_models.db_funcs import recreate_db_tables, insert_agrmnt, insert_base_retirement
from db_connect import get_db


router = APIRouter(prefix="/start", tags=["api", "start"])


@router.post("/load")
async def load_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_bytes = await file.read()
    try:
        agr_df, ret_df, _ = get_input_dfs(file_bytes)
        # print(agr_df)
        # print(ret_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await file.close()

    # load in db logic
    # recreate tables
    try:
        recreate_db_tables(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # insert data
    try:
        agr_cnt = insert_agrmnt(db, agr_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        ret_cnt = insert_base_retirement(db, ret_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "SUCCESS",
        "pandas read": {"agr": agr_df.shape[0], "ret": ret_df.shape[0]},
        "db inserted": {"agr": agr_cnt, "ret": ret_cnt},
    }
