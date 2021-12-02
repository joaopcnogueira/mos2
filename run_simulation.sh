mkdir -p figs
mkdir -p output_data

for n in $(seq 1 1 10); do
    layers="graphene+doping=0.15 ${n}H-MoS2+phonons graphene+doping=0.15"
    echo $layers
    qeh $layers --plasmons --plot --q 0.004 0.011 200 --omega 0.045 0.07 200 --saveplots Ef_0.1_MLG_"$n"MoS2_MLG.pdf
    mv *.pdf figs
    mv *.dat output_data
done
