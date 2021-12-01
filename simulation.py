from matplotlib import pyplot as plt
from qeh import make_heterostructure
import numpy as np
import argparse

parser = argparse.ArgumentParser(description = 'Gerenciador de argumentos')
parser.add_argument('-n', default='3', required=False, help='quantidade de camadas de grafeno')
args = parser.parse_args()

# layers = ['3graphene+doping=0.1,eta=1e-3']
layers_name = f'graphene+doping=0.15 {args.n}H-MoS2 graphene+doping=0.15'
layers = [layers_name]
print(layers)

# het = make_heterostructure(layers, frequencies=[1e-5, 0.2, 500],
#                            momenta=[0.0001, 0.02, 300])
# het.get_plasmon_eigenmodes(filename='graphenemodes.npz')

# data = np.load('graphenemodes.npz')

# q_q = data['q_q']
# w_w = data['omega_w']
# eig_qwl = data['eig']
# inveig_qw = - np.sum(1 / eig_qwl, axis=-1).imag

# plt.figure(figsize=(3.4, 2.5))
# plt.pcolor(q_q, w_w, inveig_qw.T)
# ax = plt.gca()
# plt.xlabel(r'$q$ (Å$^{-1}$)')
# plt.ylabel(r'$\hbar\omega$ (eV)')
# plt.tight_layout()
# plt.savefig('graphene-multilayer-modes.png', dpi=600)
