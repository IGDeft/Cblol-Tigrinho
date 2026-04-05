from fastapi import FastAPI, Body, Query
import uvicorn 
import cblol
app = FastAPI()

# GET
@app.get("/")
def home():
    return {"status": "Python API is running"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5000, reload=True)


@app.get("/ligas")
def listar_ligas():
    response = cblol.listar_todas_ligas()
    return {"ligas": response}


@app.get("/times")
def listar_times(ligas: list[str] = Query(None)):
    if not ligas:
        ligas = ["LTA S"]
    response = cblol.obter_times_liga(ligas)
    return {"times": response}

# POST
@app.post("/predict")
def predict(data: dict = Body(...)):
    print(f"Dados recebidos do Java: {data}")
    time_a = data.get("timeA")
    time_b = data.get("timeB")
    jogos = data.get("quantidadeJogos")

    response = cblol.ordemPicksBans(time_a, time_b, jogos, [])

    return {"draft": response}

