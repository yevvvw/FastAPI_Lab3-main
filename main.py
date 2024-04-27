from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routers import client, cardriver, trips
from apps import models
from apps.db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(client.router)
app.include_router(cardriver.router)
app.include_router(trips.router)

@app.get("/", response_class=HTMLResponse)
def root():
    return "<h1>lab3</h1>"