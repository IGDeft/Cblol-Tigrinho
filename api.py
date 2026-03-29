from fastapi import FastAPI
import uvicorn 
from cblol import ordemPicksBans
app = FastAPI()

@app.get("/")
def home():
    response = ordemPicksBans("LOUD", "paiN Gaming", 2, [])
    return {"status": response}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5000, reload=True)

