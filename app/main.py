from fastapi import FastAPI
from mangum import Mangum

from app.database import init_db
from app.routes.sample import router as sample_router
from app.routes.user import router as user_router
from app.routes.blackjack import router as blackjack_router

app = FastAPI()


@app.on_event("startup")
async def connect():
    await init_db()


@app.get("/")
def index():
    return {"message": "Welcome To FastAPI World"}


app.include_router(sample_router)
app.include_router(user_router)
app.include_router(blackjack_router)

handler = Mangum(app)
