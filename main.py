from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def alive():
    return {"message": "Alive"}
