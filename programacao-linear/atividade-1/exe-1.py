import pulp as p
import pandas as pd

# Dados de entrada
df = pd.DataFrame({
    'Modelo' :     ['a','b','c'],
    'mao_de_obra': [7,3,6],
    'material':    [4,4,5],
    'lucro' :      [4,2,3]
})

print(df)

modelo = p.LpProblem("Maximizar_Lucro", p.LpMaximize)

# Variáveis de decisão
decisao = {linha.Modelo: p.LpVariable(f"x_{linha.Modelo}", lowBound=0, cat='Integer')
	for linha in df.itertuples()
}

# Função objetivo
modelo += p.lpSum(decisao[i] * df.loc[df.Modelo == i, 'lucro'].iloc[0] for i in df.Modelo)

# Restrições
modelo += p.lpSum(decisao[i] * df.loc[df.Modelo == i, 'mao_de_obra'].iloc[0] for i in df.Modelo) <= 200
modelo += p.lpSum(decisao[i] * df.loc[df.Modelo == i, 'material'].iloc[0] for i in df.Modelo) <= 150

modelo.solve()

print("Status:", p.LpStatus[modelo.status])
for i in df.Modelo:
	print(f"Produzir {decisao[i].varValue} unidades do produto {i}")
print("Lucro total: R$", p.value(modelo.objective))