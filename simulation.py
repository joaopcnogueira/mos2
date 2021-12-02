from matplotlib import pyplot as plt
from qeh import make_heterostructure
import numpy as np
import argparse

parser = argparse.ArgumentParser(description = 'Gerenciador de argumentos')
parser.add_argument('-n', default='3', required=False, help='quantidade de camadas de grafeno')
args = parser.parse_args()

layers = ['graphene+doping=0.15', '3H-MoS2', 'graphene+doping=0.15']
het = make_heterostructure(layers, frequencies=[1e-5, 0.2, 200], momenta=[0.0001, 0.02, 200])
het.get_plasmon_eigenmodes(filename='graphenemodes.npz')

data = np.load('graphenemodes.npz')

q_q = data['q_q']
w_w = data['omega_w']
eig_qwl = data['eig']
inveig_qw = - np.sum(1 / eig_qwl, axis=-1).imag

nq = len(q_q)

arq_test = open('Plasmon Modes ' + str(save_plots) +'.dat', "w") 
for iq in range(nq):
    freqs = np.array(omega0[iq])
    plt.plot([q_q[iq], ] * len(freqs), freqs, 'k.')
    arq_test.write("{}".format(q_q[iq]))
    for waux in freqs:
            arq_test.write(",{}".format(waux))
    arq_test.write("\n")
    plt.ylabel(r'$\hbar\omega$ (eV)')
    plt.xlabel(r'q (Å$^{-1}$)')
arq_test.close()

# plt.figure(figsize=(3.4, 2.5))
# plt.pcolor(q_q, w_w, inveig_qw.T)
# ax = plt.gca()
# plt.xlabel(r'$q$ (Å$^{-1}$)')
# plt.ylabel(r'$\hbar\omega$ (eV)')
# plt.tight_layout()
# plt.savefig('graphene-multilayer-modes-teste.png', dpi=600)
