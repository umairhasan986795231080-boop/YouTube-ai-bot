from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "YouTube AI Bot Running"}
