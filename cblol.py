# %% [markdown]
# <a href="https://colab.research.google.com/github/IGDeft/Cblol-Tigrinho/blob/main/CblolTigrinho.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %%
import pandas as pd

tabela = pd.read_csv("2025_LoL_esports_match_data_from_OraclesElixir.csv")


# %%
print(tabela['league'].unique())
print()
print(tabela.columns.tolist())

# %%
tabela_lta_sul = tabela[tabela['league'] == "LTA S"].copy()


tabela_relev = [

    # Identificação Jogo

    'gameid', "split", "game", "patch", "date", "playoffs", "position",
    "result",

    # Jogador/Time
    "playername", "teamname", "participantid", "playerid", "kills", "deaths",
    "assists", "teamkills", "teamdeaths", "earnedgoldshare", "damageshare",

    # Pick e Ban
    "ban1", "ban2", "ban3", "ban4", "ban5", "pick1", "pick2", "pick3", "pick4",
    'pick5', "firstPick", "champion",

    # Objetivos

    "void_grubs", "towers", "turretplates", "dragons",

    # Ritmo de Jogo

    "firsttower", "firstblood", "firstdragon", "firstbaron", "firstherald",
    "gamelength", "csdiffat10", "xpdiffat10", "golddiffat10",
    "csdiffat15", "xpdiffat15", "golddiffat15",
    "team kpm", "ckpm", "cspm",
]

tabela_final = tabela_lta_sul[tabela_relev].copy()



# %%
# Global pIcks

tabela_players = tabela_final[tabela_final['position']!= "team"]
champion_global = tabela_players['champion'].value_counts()
print(champion_global.head(20))

# Global Bans

tabela_team = tabela_final[tabela_final['position'] == "team"]

bans_global = pd.concat([
    tabela_team["ban1"],
    tabela_team['ban2'],
    tabela_team['ban3'],
    tabela_team['ban4'],
    tabela_team['ban5']
])
print("-" * 20)
print("Bans")

print(bans_global.value_counts().head(20))

# Pick Rate

total_jogos = tabela_team['gameid'].nunique()
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
print(tabela_lta_sul['teamname'].unique())

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
time1 = input("1 time: ")
time2 = input("2 time: ")

df_time1 = gerar_df_time(time1)
df_time2 = gerar_df_time(time2)

if df_time1 is not None and df_time2 is not None:
    print(time1)

    print(time2)


# %%
def sugeriPicks(time1, bansTime1, picksTime1, time2, bansTime2, picksTime2, picks):
    df = gerar_df_time(time1)
    
    proibidos = list(bansTime1) + list(bansTime2) + list(picks)

    df_filtrado = df[~df.index.astype(str).isin(proibidos)]

    if df_filtrado.empty:
        return "Não existe mais personagens disponíveis"
    
    return df_filtrado.sort_values(by = "pick_rate", ascending = False).index[0]

def sugeriBans(time1, bansTime1, picksTime1, time2, bansTime2, picksTime2, picks):
    df = gerar_df_time(time1)
    proibidos = list(bansTime1) + list(bansTime2) + list(picks)

    df_filtrado = df[~df.index.astype(str).isin(proibidos)]

    if df_filtrado.empty:
        return "Não existe mais personagens disponíveis"
    
    return df_filtrado.sort_values(by = "ban_rate", ascending = False).index[0]

def gerar_Dna_Automatico(df_completo):
    contagem = df_completo.groupby(["champion", "position"]).size().unstack(fill_value = 0)
    dna_percentual = contagem.div(contagem.sum(axis = 1), axis = 0)

    return dna_percentual.to_dict(orient = "index")

dna_campeoes = gerar_Dna_Automatico(tabela_final)

# %%
def ordemPicksBans(timeFP, timeLP, jogos, picks=None):

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




