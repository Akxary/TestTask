from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from routes.main_router import router

if __name__ == "__main__":
    app = FastAPI()
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=80)
