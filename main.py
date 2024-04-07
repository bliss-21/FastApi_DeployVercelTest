from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def home():
    return {"mensaje":"hola mundo"}


