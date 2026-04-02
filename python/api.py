from fastapi import FastAPI, Body
import uvicorn 
from cblol import ordemPicksBans
app = FastAPI()

@app.post("/predict")
def predict(data: dict = Body(...)):
    print(f"Dados recebidos do Java: {data}")
    time_a = data.get("timeA")
    time_b = data.get("timeB")
    jogos = data.get("quantidadeJogos")

    response = ordemPicksBans(time_a, time_b, jogos, [])

    return {"draft": response}

@app.get("/")
def home():
    return {"status": "Python API is running"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5000, reload=True)

