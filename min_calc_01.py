import pandas as pd

df = pd.read_csv('dados/Plasmon Modes Ef_0.1_MLG_2MoS2_MLG_JOAO.pdf.dat')

df = df.dropna().assign(diff = lambda df: df['z']-df['y'])

print(f"Omega: {df['diff'].min()}")

