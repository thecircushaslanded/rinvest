from itertools import permutations

import pandas as pd

df = pd.read_csv("Hedge_cleaned2.csv")

choices = df.columns[1:]
hedges = []

for k in range(len(df)):
    broker = df.ix[k]["broker"]
    row_choices = df.loc[k].dropna().index.tolist()[1:]

    currencies = set([c[:3] for c in row_choices])
    for cur in permutations(currencies, 4):
        comb = [cur[0]+"-"+cur[1], cur[1]+"-"+cur[2], 
                cur[2]+"-"+cur[3], cur[3]+"-"+cur[0]]
        if all([(col in row_choices) for col in comb]):
            p1, p2, p3, p4 = comb
            ret = sum(df.ix[k].loc[comb])
            hedges.append([broker, p1, p2, p3, p4, ret])
                    
"""
sort!(hedges, cols=[:r], rev=true)
print(hedges)

broker_ret = sort!(by(hedges, [:broker], df -> median(df[:ret])), cols=[:x1], rev=true)
pos_ret = sort!(hedges[hedges[:ret] .> 1e-8, :], cols=[:ret], rev=true)
broker_ret = sort!(by(pos_ret, [:broker], df -> size(df)[1](df[:ret])), cols=[:x1], rev=true)"""
