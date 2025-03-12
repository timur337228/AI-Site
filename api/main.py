from fastapi import FastAPI
from authx import A

app = FastAPI()


@app.post('/login')
def login():
    ...


@app.get('/protected')
def protected():
    ...
