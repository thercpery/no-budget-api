from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {
        "message": "No-Budget Shop API: We'll drain your wallet more by selling second-hand products that you don't need."
    }
