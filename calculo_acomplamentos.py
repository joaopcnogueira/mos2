import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from feature_engine.wrappers import SklearnTransformerWrapper
from sklearn.cluster import DBSCAN

omega_df = pd.DataFrame()
for qtd_camadas_tmd in range(20, 31, 10):
    filename = f"output_data/Plasmon Modes Ef_0.1_MLG_{qtd_camadas_tmd}MoS2_MLG.pdf.dat"
    dat = pd.read_csv(filename, header=None)

    # primeiro passo: remover colunas com baixa variância
    features = dat.drop([0], axis=1).describe().loc['std'].sort_values(ascending=False).index.tolist()[0:2]
    dat = dat.filter(features)
    dat.columns = ['w1', 'w2']

    # segundo passo: remover colunas com baixa variância
    dat = dat.dropna()

    # terceiro passo: clustering
    dat['x'] = range(1, len(dat) +1)
    dat_melt = dat.melt(id_vars=['x'])
    scaler = SklearnTransformerWrapper(MinMaxScaler(feature_range=(0, 0.01)), variables='x')
    dat_melt = scaler.fit_transform(dat_melt)
    dbscan = DBSCAN(eps=0.0006, min_samples=5)
    dbscan.fit(dat_melt[['x', 'value']])
    dat_melt['cluster_id'] = dbscan.labels_
#    if qtd_camadas_tmd <= 10:
#        selected_clusters = dat_melt.value_counts("cluster_id").index.tolist()[0:2]
#    else:
#        selected_clusters = dat_melt.pivot(index='x', columns='cluster_id', values='value').describe().loc['std'].sort_values(ascending=False).index.tolist()[0:2]
    selected_clusters = dat_melt.pivot(columns='cluster_id', values='value').drop(-1, axis=1, errors='ignore').describe().loc['std'].sort_values(ascending=False).index.tolist()[0:2]
    dat_melt = dat_melt.query(f"cluster_id in {selected_clusters}")
    dat2 = dat_melt.drop(['cluster_id'], axis=1).pivot(index='x', columns='variable').rename_axis('', axis=0)
    dat2.columns = ['w1', 'w2']

    # quarto passo: calculando e salvando o acoplamento
    omega = np.min(np.abs(dat2['w1'] - dat2['w2']))
    omega_df = omega_df.append([{'n': qtd_camadas_tmd, 'omega': omega}], ignore_index=True)


omega_df.plot(x='n', y='omega', kind='scatter', backend='plotly')

# saving the data
omega_df.to_csv('output_data/omega_20_to_30.csv', index=False)    
