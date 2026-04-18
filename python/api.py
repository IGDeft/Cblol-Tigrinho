from fastapi import FastAPI, Body, Query
from draft import Fase, proxima_fase
import uvicorn 
import cblol
import uuid

app = FastAPI()

sessions = {}

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

@app.post("/draft/iniciar")
def iniciar_draft(data: dict = Body(...)):
    session_id = str(uuid.uuid4())

    if(data["isFirstPick"]):
        jogador_atual = "PLAYER"
    else:
        jogador_atual = "IA"

    sessions[session_id] = {
        "total_jogos": data["quantidadeJogos"],
        "is_first_pick": data["isFirstPick"],
        "time_user": data["timeUsuario"],
        "time_ia": data["timeIA"],
        "game_atual": 1,
        "fase_atual": "BAN_1",
        "jogador_atual": jogador_atual,
        "bans": {"player": [], "ia": []},
        "picks": {"player": [], "ia": []},
    }
    return {"sessionId": session_id, "faseAtual": "BAN_1", "jogadorAtual": jogador_atual}

@app.post("/draft/acao")
def acao_draft(data: dict = Body(...)):
    state = sessions[data["sessionId"]]
    is_ban = state["fase_atual"].startswith("BAN")
    picks = state["picks"]["player"] + state["picks"]["ia"]

    if(state["jogador_atual"] == "PLAYER"):
        if(is_ban):
            state["bans"]["player"].append(data["champion"])
        else:
            state["picks"]["player"].append(data["champion"])
    else:
        args = (
            state["time_ia"], state["bans"]["ia"], state["picks"]["ia"], state["time_user"], state["bans"]["player"], state["picks"]["player"], picks
            )
        if(is_ban):
            champion = cblol.sugeriBans(*args)
            state["bans"]["ia"].append(champion)
        else:
            champion = cblol.sugeriPicks(*args)
            state["picks"]["ia"].append(champion)

    fase_atual = Fase(state["fase_atual"])
    proxima, jogador = proxima_fase(fase_atual, state["is_first_pick"])

    state["fase_atual"] = proxima.value
    state["jogador_atual"] = jogador
    tem_mais_jogos = True
    if(state["game_atual"] == state["total_jogos"]):
        if(proxima == Fase.FIM):
            tem_mais_jogos: bool = False
    return{
        "sessionId": data["sessionId"],
        "faseAtual": state["fase_atual"],
        "jogadorAtual": state["jogador_atual"],
        "bansPlayer": state["bans"]["player"],
        "bansIA": state["bans"]["ia"],
        "picksPlayer": state["picks"]["player"],
        "picksIA": state["picks"]["ia"],
        "fearless": picks,
        "temMaisJogos": tem_mais_jogos
    }    

