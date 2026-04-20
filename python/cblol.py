# %% [markdown]
# <a href="https://colab.research.google.com/github/IGDeft/Cblol-Tigrinho/blob/main/CblolTigrinho.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %%
import pandas as pd

tabela = pd.read_csv("2025_LoL_esports_match_data_from_OraclesElixir.csv")
#display(tabela)

# %%
print(tabela['league'].unique())
print()
print(tabela.columns.tolist())

# %%
def obter_times_liga(lista_liga = None):

  if lista_liga is None:
    return tabela['teamname'].unique()
  
  if isinstance(lista_liga, str):
    lista_liga = [lista_liga]
  
  todos_times = []

  for liga in lista_liga:
    filtro = tabela[tabela['league'] == liga]
    times_da_liga = filtro['teamname'].unique().tolist()
    todos_times.extend(times_da_liga)

  return sorted(list(set(todos_times)))

def obter_campeoes():
    campeoes = tabela['champion'].dropna().unique().tolist()
    return sorted(campeoes)
# %%
def obter_tabela_liga(lista_liga = None):
  if lista_liga is None:
    return tabela
  
  if isinstance(lista_liga, str):
    lista_liga = [lista_liga]
  
  tabela_filtrada = tabela[tabela['league'].isin(lista_liga)]

  return tabela_filtrada

# %%
def listar_todas_ligas():
  return sorted(tabela['league'].unique().tolist())

# %%
#tabela_lta_sul = tabela[tabela['league'] == "LTA S"].copy()
# display(tabela_lta_sul)

tabela_relev = [

    # Identificação Jogo

    'gameid', "split", "game", "patch", "date", "playoffs", "position",
    "result", "league",
    # Jogador/Time
    "playername", "teamname", "participantid", "playerid", "kills", "deaths",
    "assists", "teamkills", "teamdeaths", "earnedgoldshare", "damageshare",

    # Pick e Ban
    "ban1", "ban2", "ban3", "ban4", "ban5", "pick1", "pick2", "pick3", "pick4",
    'pick5', "firstPick", "champion", "side",

    # Objetivos

    "void_grubs", "towers", "turretplates", "dragons",

    # Ritmo de Jogo

    "firsttower", "firstblood", "firstdragon", "firstbaron", "firstherald",
    "gamelength", "csdiffat10", "xpdiffat10", "golddiffat10",
    "csdiffat15", "xpdiffat15", "golddiffat15",
    "team kpm", "ckpm", "cspm",
]
ligas_relev = ["LTA S", "LCK", "LPL", "LEC", "LTA N", "PCS", "VCS", "LJL", "LCP", "MSI", "EWC"]

tabela_filtrada = obter_tabela_liga(ligas_relev)
tabela_final = tabela_filtrada[tabela_relev].copy()

tabela_final["gamelength"] = pd.to_timedelta(tabela_final["gamelength"], unit = 's')
tabela_final["gamelength"] = (tabela_final["gamelength"] + pd.to_datetime("1970-01-01")).dt.strftime("%H:%M:%S")
tabela_final["teamname"] = tabela_final["teamname"].replace("Isurus Estral", "Isurus")


#display(tabela_final)

# %%
print("Quantida de jogos por liga.")
jogos_por_liga = tabela_final.groupby("league")["gameid"].nunique()

print(jogos_por_liga.sort_values(ascending = False))

# %%
# Global pIcks

liga_ativa = "LTA S"
tabela_liga_ativa = tabela_final[tabela_final["league"] == liga_ativa].copy()

tabela_players_ativo = tabela_liga_ativa[tabela_liga_ativa["position"] != "team"]
tabela_team_ativo = tabela_liga_ativa[tabela_liga_ativa["position"] == "team"]


champion_global = tabela_players_ativo["champion"].value_counts()
print(champion_global.head(40))

# Global Bans

#tabela_team = tabela_final[tabela_final['position'] == "team"]

bans_global = pd.concat([
    tabela_team_ativo["ban1"],
    tabela_team_ativo['ban2'],
    tabela_team_ativo['ban3'],
    tabela_team_ativo['ban4'],
    tabela_team_ativo['ban5']
])
print("-" * 20)
print("Bans")

print(bans_global.value_counts().head(20))

# Pick Rate

total_jogos = tabela_team_ativo['gameid'].nunique()
pick_rate = (champion_global / total_jogos) * 100

print("-" * 20)
print("Pick Rate")

print(pick_rate.head(20).round(2))

# Ban Rate

ban_rate = (bans_global.value_counts()/ total_jogos) * 100

print("-" * 20)
print("Ban Rate")
print(ban_rate.head(20).round(2))

# %%
df_meta = pd.DataFrame({
    "pick_rate": pick_rate,
    "ban_rate": ban_rate
}).fillna(0)

df_meta['presence'] = df_meta["pick_rate"] + df_meta["ban_rate"]
df_meta = df_meta.sort_values(by="presence", ascending = False)
print(df_meta.head(50).round(2))

# %%
def gerar_df_time(nome_time):
    tabela_equipes = tabela_final[tabela_final["teamname"] == nome_time].copy()
    if tabela_equipes.empty:
        print(f"Time {nome_time} não foi encontrado.")
        return None
    
    picks = tabela_equipes['champion'].value_counts()

    tabela_team = tabela_equipes[tabela_equipes["position"] == "team"]

    bans = pd.concat([
        tabela_team["ban1"],
        tabela_team["ban2"],
        tabela_team["ban3"],
        tabela_team["ban4"],
        tabela_team["ban5"]
    ]).value_counts()

    total_jogos = tabela_team["gameid"].nunique()

    if total_jogos == 0:
        print(f"Time {nome_time} não tem jogos validos")
        return None
    
    df_time = pd.DataFrame({
        "picks" : picks,
        "bans" : bans
    }).fillna(0)

    df_time["pick_rate"] = (df_time["picks"] / total_jogos) * 100
    df_time["ban_rate"] = (df_time["bans"] / total_jogos) * 100
    df_time["presenca"]= (df_time["pick_rate"] + df_time["ban_rate"])

    df_time = df_time.sort_values(by = "presenca", ascending = False)
    return df_time.round(2)


# %%
mapa_dna = tabela_liga_ativa[tabela_liga_ativa["position"] != "team"].set_index(["gameid", "teamname", "champion"])["position"].to_dict()

df_agrupados = tabela_liga_ativa.groupby([
    "gameid", "teamname", "result", "firstPick", "game",
    "ban1", "ban2", "ban3", "pick1", "pick2",
    "pick3", "ban4", "ban5", "pick4", "pick5",
]).size().reset_index() 

df_confronto = pd.merge(df_agrupados, df_agrupados, on = ["gameid", "game"], suffixes = ("_time1", "_time2"))
df_confronto = df_confronto[df_confronto["teamname_time1"] != df_confronto["teamname_time2"]]
df_confronto = df_confronto.drop_duplicates(subset = ["gameid"], keep = "first")

for i in range(1, 6):
    for t in ["time1", "time2"]:
        p_col = f"pick{i}_{t}"
        r_col = f"rota_p{i}_{t}"
        df_confronto[r_col] = df_confronto.apply(
            lambda row: mapa_dna.get((row["gameid"], row[f"teamname_{t}"], row[p_col]), "desconhecido"), axis = 1
        )

#display(df_confronto)

# %%
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Pesos

bloco_treino = []
pesos = {
    "LTA S": 5, "LCK": 3, "LPL": 3, "LEC": 2,
    "LTA N": 2, "PCS": 1, "VCS": 1, "LJL": 1,
    "LCP": 1, "MSI": 4, "EWC": 4,
}

for liga, peso in pesos.items():
    dados_da_liga = tabela_final[tabela_final["league"] == liga]

    if dados_da_liga.empty:
        print(f"Os dados da liga {liga} não estão na sua base de dados.")
        continue

    for _ in range(peso):
        bloco_treino.append(dados_da_liga)

tabela_ml = pd.concat(bloco_treino).reset_index(drop = True)

# Codificadores

cod_time = LabelEncoder()
cod_pos = LabelEncoder()
cod_camp = LabelEncoder()

todos_os_times = list(tabela_ml["teamname"].unique()) + ["Desconhecidos"]
cod_time.fit(todos_os_times)

tabela_ml["teamname_num"] = cod_time.transform(tabela_ml["teamname"])
tabela_ml["position_num"] = cod_pos.fit_transform(tabela_ml["position"])
tabela_ml["champion_num"] = cod_camp.fit_transform(tabela_ml["champion"])

# Mapeamento dos Times

def extrair_parceiros(row):
    lista = row["champion_num_list"]
    atual = row["champion_num"]
    teammates = sorted([champ for champ in lista if champ != atual])

    while len(teammates) < 4:
        teammates.append(-1)

    return pd.Series(teammates[:4])

def mapear_oponentes(df):
    resumo = df.groupby(["gameid", "teamname"])["champion_num"].apply(list).reset_index()
    resumo.columns = ["gameid", "teamname", "champ_list"]

    merged = resumo.merge(resumo, on = "gameid", suffixes = ("", "_adv"))
    merged = merged[merged["teamname"] != merged["teamname_adv"]]

    def preenchido(lst):
        lst = list(lst)
        while len (lst) < 5:
            lst.append(-1)
        return lst[:5]
    
    op_cols = pd.DataFrame(merged["champ_list_adv"].apply(preenchido).tolist(), index = merged.index)
    op_cols.columns = ["o1", "o2", "o3", "o4", "o5"]

    return pd.concat([merged[["gameid", "teamname"]], op_cols], axis = 1)

# Tabela IA

df_aliado = tabela_ml.groupby(["gameid", "teamname"])["champion_num"].apply(list).reset_index()
tabela_ia = pd.merge(tabela_ml, df_aliado, on = ["gameid", "teamname"], how = "left", suffixes = ("", "_list"))

tabela_ia[["p1", "p2", "p3", "p4"]] = tabela_ia.apply(extrair_parceiros, axis = 1)

df_inimigos = mapear_oponentes(tabela_ml)
tabela_ia = pd.merge(tabela_ia, df_inimigos, on = ["gameid", "teamname"], how = "left")

# Oponentes

df_agrupados_global = tabela_ml.groupby([
    "gameid", "teamname", "result", "firstPick", "game",
    "ban1", "ban2", "ban3", "pick1", "pick2",
    "pick3", "ban4", "ban5", "pick4", "pick5"
]).size().reset_index()

df_confronto_global = pd.merge(df_agrupados_global, df_agrupados_global, on = ["gameid", "game"], suffixes = ("_time1", "_time2"))
df_confronto_global = df_confronto_global[df_confronto_global["teamname_time1"] != df_confronto_global["teamname_time2"]]
df_confronto_global = df_confronto_global.drop_duplicates(subset = ["gameid"], keep = "first")

oponentes_t1 = df_confronto_global[["gameid", "teamname_time1", "teamname_time2"]].rename(
    columns = {"teamname_time1": "teamname", "teamname_time2": "oponente"})

oponentes_t2 = df_confronto_global[["gameid", "teamname_time2", "teamname_time1"]].rename(
    columns = {"teamname_time2": "teamname", "teamname_time1": "oponente"}
)

df_relacao_oponente = pd.concat([oponentes_t1, oponentes_t2])

tabela_ia = pd.merge(tabela_ia, df_relacao_oponente, on = ["gameid", "teamname"], how = "left")
tabela_ia["oponente"] = tabela_ia["oponente"].fillna("Desconhecidos").astype(str)
tabela_ia["oponente_num"] = cod_time.transform(tabela_ia["oponente"])

tabela_ia = pd.merge(tabela_ia, df_meta.reset_index().rename(columns = {"index": "champion"}), on = "champion", how = "left").fillna(0)

tabela_ia["num_picks"] = tabela_ia.groupby("gameid").cumcount()

# Treino IA

colunas_treino = [
    "teamname_num", "oponente_num", "pick_rate", "presence",
    "num_picks", 
    "p1", "p2", "p3", "p4",
    "o1", "o2", "o3", "o4", "o5"
]

X = tabela_ia[colunas_treino]
y = tabela_ia["champion_num"]

# modelo_ia = RandomForestClassifier(
#     n_estimators = 300,
#     max_depth = 15,
#     min_samples_leaf = 2,
#     random_state = 42
# )

# modelo_ia.fit(X, y)

# print(f"IA treinada com sucesso! Liga ativa {liga_ativa} | Linhas de treino: {len(tabela_ml)}")


# %%
p1_t1 = df_confronto[df_confronto["firstPick_time1"] == 1][["teamname_time1", "pick1_time1"]].rename(
    columns = {"teamname_time1": "teamname", "pick1_time1": "pick1"}
)
p1_t2 = df_confronto[df_confronto["firstPick_time2"] == 1][["teamname_time2", "pick1_time2"]].rename(
    columns = {"teamname_time2": "teamname", "pick1_time2": "pick1"}
)

df_p1_unificado = pd.concat([p1_t1, p1_t2])

prioridade_p1 = df_p1_unificado.groupby(["teamname", "pick1"]).size().unstack(fill_value = 0)
prioridade_p1 = prioridade_p1.div(prioridade_p1.sum(axis = 1), axis = 0).fillna(0)


# %%
dados_players_global = tabela_final[tabela_final["position"] != "team"]
tabela_times_global = tabela_final[tabela_final["position"] == "team"]

contagem_pares = {}
contagem_exposicao = {}
contagem_respostas = {}

for (gameid, teamname), grupo in dados_players_global.groupby(["gameid", "teamname"]):
    champ = grupo["champion"].tolist()

    for i in range(len(champ)):
        for j in range(i + 1, len(champ)):
            par = tuple(sorted([champ[i], champ[j]]))
            contagem_pares[par] = contagem_pares.get(par, 0) + 1

for gameid, jogo in dados_players_global.groupby(["gameid"]):
    times = jogo["teamname"].unique()

    if len(times) != 2:
        continue

    camp_t1 = jogo[jogo["teamname"] == times[0]]["champion"].tolist()
    camp_t2 = jogo[jogo["teamname"] == times[1]]["champion"].tolist()

    for picks_inimigo, picks_aliado in ([camp_t1, camp_t2], [camp_t2, camp_t1]):

        for inimigo in picks_inimigo:
            contagem_exposicao[inimigo] = contagem_exposicao.get(inimigo, 0) + 1

        for resposta in picks_aliado:
            par = (inimigo, resposta)

            contagem_respostas[par] = contagem_respostas.get(par, 0) + 1

ban_fase2_por_pick = {}
total_pick_fase2 = {}

for gameid, jogo_team in tabela_times_global.groupby("gameid"):
    times = jogo_team["teamname"].unique()

    if len(times) != 2:
        continue

    for time in times:
        picks_time = dados_players_global[
            (dados_players_global["gameid"] == gameid) & (dados_players_global["teamname"] == time)
        ]["champion"].tolist()

        ban_fase2 = jogo_team[jogo_team["teamname"] == time][["ban4", "ban5"]].values.flatten().tolist()

        for pick in picks_time:
            total_pick_fase2[pick] = total_pick_fase2.get(pick, 0) + 1

            for ban in ban_fase2:
            
                if pd.notna(ban):
                    ban_fase2_por_pick[(pick, ban)] = ban_fase2_por_pick.get((pick, ban), 0) + 1


print(f"Pares: {len(contagem_pares)}")
print(f"Exposição: {len(contagem_exposicao)}")
print(f"ban fase 2: {len(ban_fase2_por_pick)}")

# %%
limiar_flex = 0.10
minimo_exposicao = 3
limitar_ban_proprio = 0.10


def gerar_Dna_Automatico(df_completo):
    contagem = df_completo.groupby(["champion", "position"]).size().unstack(fill_value = 0)
    dna_percentual = contagem.div(contagem.sum(axis = 1), axis = 0)
    return dna_percentual.to_dict(orient = "index")
dna_campeoes = gerar_Dna_Automatico(tabela_liga_ativa)


def get_posicoes_ocupadas(lista_picks, dna_campeoes):
    candidatos = {}
    
    for pick in lista_picks:
        if pick not in dna_campeoes:
            continue

        for rota, pct in dna_campeoes[pick].items():
            if pct > limiar_flex:
                candidatos.setdefault(rota, []).append((pick, pct))

    rotas_ocupadas = {}
    picks_alocados = set()

    # Garantido não flex

    ordem = sorted(
        candidatos.items(),
        key = lambda x: max(p for _, p in x[1]),
        reverse = True
    )

    for rota, lista in ordem:
        list_ord = sorted(lista, key = lambda x: x[1], reverse = True)

        for camp, pct in list_ord:

            if camp not in picks_alocados:
                rotas_ocupadas[rota] = camp
                picks_alocados.add(camp)
                break

    return list(rotas_ocupadas.keys())       

def sugeriPicks(time1, bansTime1, picksTime1, time2, bansTime2, picksTime2, picks):
    df = gerar_df_time(time1)
    
    proibidos = list(bansTime1) + list(bansTime2) + list(picks)

    df_filtrado = df[~df.index.astype(str).isin(proibidos)]

    if df_filtrado.empty:
        return "Não existe mais personagens disponíveis"
    
    rota_time = get_posicoes_ocupadas(picksTime1, dna_campeoes)

    def rota_livre(nome_champ):
        if nome_champ not in dna_campeoes:
            return False
        
        pos_preferida = max(dna_campeoes[nome_champ], key = dna_campeoes[nome_champ].get)

        if pos_preferida in rota_time:
            return False # está cheio
        else:
            return True # tem vaga
        
    candidatos_pos = df_filtrado[df_filtrado.index.map(rota_livre)]

    if not candidatos_pos.empty:
        return candidatos_pos.sort_values(by = "pick_rate", ascending = False).index[0]
    
    return df_filtrado.sort_values(by = "pick_rate", ascending = False).index[0]
    

def sugeriBans(time1, bansTime1, picksTime1, time2, bansTime2, picksTime2, picks):
    df = gerar_df_time(time1)
    proibidos = list(bansTime1) + list(bansTime2) + list(picks)

    df_filtrado = df[~df.index.astype(str).isin(proibidos)]

    if df_filtrado.empty:
        return "Não existe mais personagens disponíveis"
    
    rota_adv = get_posicoes_ocupadas(picksTime2, dna_campeoes)

    def ban_valido(nome_champ):
        if nome_champ not in dna_campeoes:
            return True
        
        pos_advprincipal = max(dna_campeoes[nome_champ], key = dna_campeoes[nome_champ].get)

        if pos_advprincipal in rota_adv:
            return False
        else:
            return True
        
    candidatos_ban = df_filtrado[df_filtrado.index.map(ban_valido)]

    if not candidatos_ban.empty:
        return candidatos_ban.sort_values(by = "ban_rate", ascending = False).index[0]
    
    return df_filtrado.sort_values(by = "ban_rate", ascending = False).index[0]

# %%
def ordemPicksBans(timeFP, timeLP, jogos, picks = None):

  if picks is None:
    picks = []

  picksFP, bansFP = [], []
  picksLP, bansLP = [], []

  bans = []

  for _ in range(3):
    ban = sugeriBans(timeFP, bansFP, picksFP, timeLP, bansLP, picksLP, picks)
    bans.append(ban)
    bansFP.append(ban)

    ban = sugeriBans(timeLP, bansLP, picksLP, timeFP, bansFP, picksFP, picks)
    bans.append(ban)
    bansLP.append(ban)

  ordem = [timeFP, timeLP, timeLP, timeFP, timeFP, timeLP]

  for time_atual in ordem:
    if time_atual == timeFP:
      champ = sugeriPicks(timeFP, bansFP, picksFP, timeLP, bansLP, picksLP, picks)
      picksFP.append(champ)
    else:
      champ = sugeriPicks(timeLP, bansLP, picksLP, timeFP, bansFP, picksFP, picks)
      picksLP.append(champ)

    picks.append(champ)

  for _ in range(2):
    ban = sugeriBans(timeLP, bansLP, picksLP, timeFP, bansFP, picksFP, picks)
    bans.append(ban)
    bansLP.append(ban)

    ban = sugeriBans(timeFP, bansFP, picksFP, timeLP, bansLP, picksLP, picks)
    bans.append(ban)
    bansFP.append(ban)

  ordem2 = [timeLP, timeFP, timeFP, timeLP]

  for time_atual in ordem2:

    if time_atual == timeFP:
      champ = sugeriPicks(timeFP, bansFP, picksFP, timeLP, bansLP, picksLP, picks)
      picksFP.append(champ)
    else:
      champ = sugeriPicks(timeLP, bansLP, picksLP, timeFP, bansFP, picksFP, picks)
      picksLP.append(champ)

    picks.append(champ)

  jogo_atual = [picksFP, bansFP, picksLP, bansLP]

  if jogos > 1:
    return [jogo_atual] + ordemPicksBans(timeFP, timeLP, jogos-1, picks)
  
  return [jogo_atual]

# %%
times_liga_ativa = tabela_liga_ativa["teamname"].unique()

print(times_liga_ativa)

# %%
time1 = "LOUD"
time2 = "FURIA"

# 1. Criamos uma lista vazia para acompanhar o histórico da série toda
historico_fearless = []

# 2. Rodamos o draft (os picks ficam acumulados na recursão)
resultado_serie = ordemPicksBans(time1, time2, 5) 

# 3. EXIBIÇÃO ORGANIZADA
for i, jogo in enumerate(resultado_serie):
    pFP, bFP, pLP, bLP = jogo
    
    # Adicionamos os picks desse jogo ao nosso histórico de visualização
    # Somamos picks de ambos os times
    picks_do_jogo = pFP + pLP
    historico_fearless.extend(picks_do_jogo)

    print(f"{'#'*2}  JOGO {i + 1}  {'#'*1}")

    # EXIBIÇÃO DOS BANS
    print(f"🚫 BANS: {time1}: {', '.join(bFP)} | {time2}: {', '.join(bLP)}")

    # EXIBIÇÃO DOS PICKS
    print(f"{'='*16} ⚔️  COMPOSIÇÕES FINAIS ⚔️  {'='*16}")
    print(f"{time1:<28} | {time2:>28}")
    print("-" * 60)
    for j in range(5):
        c1 = pFP[j] if j < len(pFP) else "---"
        c2 = pLP[j] if j < len(pLP) else "---"
        print(f"P{j+1}: {c1:<24} | P{j+1}: {c2:>24}")
    print("-" * 60)

    # 4. EXIBIÇÃO DOS CAMPEÕES "QUEIMADOS" (Fearless)
    # Mostra apenas o que já foi usado ATÉ o jogo anterior
    if i > 0:
        usados_antes = historico_fearless[:-10] # Tira os 10 picks do jogo atual
        print(f"⚠️  FEARLESS (Já usados na série):")
        print(f"[{', '.join(usados_antes)}]")
        print("-" * 60)

# %%
#time1 = input("1 time: ")
#time2 = input("2 time: ")
time1 = "LOUD"
time2 = "FURIA"
df_time1 = gerar_df_time(time1)
df_time2 = gerar_df_time(time2)

if df_time1 is not None and df_time2 is not None:
    print(time1)
    # display(df_time1.head(10))
    print(time2)
    # display(df_time2.head(10))


