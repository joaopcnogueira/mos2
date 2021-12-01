import os
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description = 'Gerenciador de Simulações/Experimentos')
parser.add_argument('-n', default='5', required=False, help='quantidade de simulações')
args = parser.parse_args()

for n in range(1, int(args.n)+1):
    os.system(f'python simulation.py -n {n}')
