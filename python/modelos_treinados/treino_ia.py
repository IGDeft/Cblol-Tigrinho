import os
import sys
import joblib

pasta_treino = os.path.dirname(os.path.abspath(__file__))
pasta_python = os.path.dirname(pasta_treino)

sys.path.append(pasta_python)
os.chdir(pasta_python)

import cblol

ligas = ["CBLOL", "LCK", "LPL", "LEC", None]

for l in ligas:
    print(f"\nTreinamento liga: {l if l else 'Geral (Sem bônus)'}")

    modelo = cblol.treinar_modelo(l)
    nome_arquivo = f"modelo_{l.upper()}.joblib" if l else "modelo_GERAL.joblib"

    saida = os.path.join(pasta_treino, nome_arquivo)
    joblib.dump(modelo, saida)

print(f"\nTreinamento de todas as ligas concluidos.")