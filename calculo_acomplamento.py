import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from feature_engine.wrappers import SklearnTransformerWrapper
from sklearn.cluster import DBSCAN

qtd_tmds = 40
dat = pd.read_csv(f'output_data/Plasmon Modes Ef_0.1_MLG_{qtd_tmds}MoS2_MLG.pdf.dat', header=None)
dat.plot(kind='scatter', x=0, y=list(range(1, 44)), backend='plotly')

# primeiro passo: remover colunas com baixa variância
features = dat.drop([0], axis=1).describe().loc['std'].sort_values(ascending=False).index.tolist()[0:2]
dat = dat.filter(features)
dat.columns = ['w1', 'w2']
dat.plot(kind='scatter', y=['w1', 'w2'], backend='plotly')

# segundo passo: dropna()
dat = dat.dropna()
dat.plot(kind='scatter', y=['w1', 'w2'], backend='plotly')

# terceiro passo: clustering
dat['x'] = range(1, len(dat) +1)
dat_melt = dat.melt(id_vars=['x'])

from sklearn.preprocessing import MinMaxScaler
from feature_engine.wrappers import SklearnTransformerWrapper
scaler = SklearnTransformerWrapper(MinMaxScaler(feature_range=(0, 0.01)), variables='x')
dat_melt = scaler.fit_transform(dat_melt)

dat_melt.plot(x='x', y='value', kind='scatter')

from sklearn.cluster import DBSCAN
dbscan = DBSCAN(eps=0.007, min_samples=5)
dbscan.fit(dat_melt[['x', 'value']])

import matplotlib.pyplot as plt
plt.figure(figsize=(10,7))
plt.scatter(dat_melt['x'], dat_melt['value'], c=dbscan.labels_, s=30, cmap='cividis')
dat_melt['cluster_id'] = dbscan.labels_

selected_clusters = dat_melt.pivot(columns='cluster_id', values='value').drop(-1, axis=1, errors='ignore').describe().loc['std'].sort_values(ascending=False).index.tolist()[0:2]
# selected_clusters = dat_melt.value_counts("cluster_id").index.tolist()[0:2]

dat_melt = dat_melt.query(f"cluster_id in {selected_clusters}")
dat_melt.plot(x='x', y='value', kind='scatter')

dat2 = dat_melt.drop(['cluster_id'], axis=1).pivot(index='x', columns='variable').rename_axis('', axis=0)
dat2.columns = ['w1', 'w2']
np.min(np.abs(dat2['w1'] - dat2['w2']))
