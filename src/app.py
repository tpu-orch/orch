from fastapi import FastAPI
from handler import router

app = FastAPI()
app.include_router(router)
