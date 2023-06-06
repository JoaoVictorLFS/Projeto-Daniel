# Importando a biblioteca numpy para usar a função exp
import numpy as np

# Definindo uma função que calcula a probabilidade de vitória de um time
def prob_vitoria(time1, time2):
  # Calculando a diferença de gols entre os times
  dif_gols = time1["gols_pro"] - time1["gols_contra"] - (time2["gols_pro"] - time2["gols_contra"])
  # Calculando a probabilidade de vitória usando uma função exponencial
  prob = 1 / (1 + np.exp(-dif_gols))
  # Retornando a probabilidade
  return prob

# Definindo os dados dos times (gols pró e gols contra)
flamengo = {"gols_pro": 14, "gols_contra": 10}
gremio = {"gols_pro": 12, "gols_contra": 11}

# Calculando e imprimindo a probabilidade de vitória do Flamengo sobre o Grêmio
prob_flamengo = prob_vitoria(flamengo, gremio)
print(f"A probabilidade de vitória do Flamengo sobre o Grêmio é de {prob_flamengo:.2f}")
