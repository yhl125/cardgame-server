from fastapi import FastAPI
from mangum import Mangum

from database import init_db
from routes.sample import router as sample_router

app = FastAPI()


@app.on_event("startup")
async def connect():
    await init_db()


@app.get("/")
def index():
    return {"message": "Welcome To FastAPI World"}


app.include_router(sample_router)

handler = Mangum(app)
