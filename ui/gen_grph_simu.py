import networkx as nx
import random
from gen_grph_simu import *
import matplotlib.pyplot as plt
import pandas as pd

"""
# EXTRACTING DATA FROM A FILE
file_path = "/Users/user/Documents/datasets/CapeVerdeReferenceSystemData_v001/SantiagoData_v2.xlsx"



line_id = pd.read_excel(file_path, sheet_name="Line Data", usecols="A").to_numpy()
depart = pd.read_excel(file_path, sheet_name="Line Data", usecols="B").to_numpy()
destination = pd.read_excel(file_path, sheet_name="Line Data", usecols="C").to_numpy()
length = pd.read_excel(file_path, sheet_name="Line Data", usecols="F").to_numpy()
resistance = pd.read_excel(file_path, sheet_name="Line Data", usecols="G").to_numpy()
customers = pd.read_excel(file_path, sheet_name="Customers", usecols="A").to_numpy()
trad_generators = pd.read_excel(file_path, sheet_name="Traditional Generators", usecols="A").to_numpy()
renw_generators = pd.read_excel(file_path, sheet_name="Renewable Generators", usecols="A").to_numpy()

sommets = [i+1 for i in range(106)]
aretes = [(depart[i][0], destination[i][0]) for i in range(len(depart))]
puits = []
sources = [1, 3, 7, 8, 9, 10, 12, 56, 74, 76, 77]

for i in range(len(customers)):
    if i==0:
        continue
    puits.append(customers[i][0])




puits.append(59)
puits.append(96)
puits.append(97)
#sources = list(set(sources))
puits = list(set(puits))
#sources.sort()
puits.sort()
inter = sommets.copy()
# [59, 97, 96]
for i in sources:
    if i in inter:
        inter.remove(i)
for i in puits:
    if i in inter:
        inter.remove(i)



# inv cost
cost_inv_1 = {
    j: random.randint(10, 50) for j in aretes
}

i_capacity_1 = {
    j: random.randint(10, 100) for j in aretes
}

max_capacity_1 = {
    j: random.randint(200, 500) for j in aretes
}

# T c l'horizon
# period c de l'intervalle en années
T_1 = 15
period_1 = [i+1 for i in range(T_1)]
demand_1 = {
    j: random.randint(50, 500) for j in period_1
}

cost_flow_1 = {
    j: random.randint(10, 100) for j in aretes
}



G = nx.DiGraph(aretes)
pos = nx.spring_layout(G)
nx.draw(G, pos=pos)

nx.draw_networkx_labels(G, pos, font_family="sans-serif")
nx.draw_networkx_nodes(G, pos, nodelist=puits, node_size=400,
                       node_color="blue")
nx.draw_networkx_nodes(G, pos, nodelist=sources, node_size=400,
                       node_color="red")

nx.draw_networkx_nodes(G, pos, nodelist=inter, node_size=400,
                       node_color="orange")
plt.show()

"""
# simulation

# if p small use fast_gnp_random_graph(), else use gnp_random_graph()

#random.seed(10)


G = nx.erdos_renyi_graph(100, 0.3, seed=None, directed=True)

edges = G.edges
nodes = G.nodes

# pr c proba de choisir les sommets qui seront départs
pr = 0.2
s = list(set([random.randrange(0, int(len(nodes)/2)) for i in range(int(len(nodes)*pr))]))
p = list(set([random.randrange(int(len(nodes)/2), len(nodes)) for i in range(int(len(nodes)*pr))]))



# inv cost
cost_inv = {
    j: random.randint(10, 100) for j in edges
}

i_capacity = {
    j: random.randint(10, 100) for j in edges
}

max_capacity = {
    j: random.randint(200, 500) for j in edges
}
# T c l'horizon
# period c de l'intervalle en années
T = 15
period = [i+1 for i in range(T)]
demand = {
    j: random.randint(50, 500) for j in period
}

cost_flow = {
    j: random.randint(10, 100) for j in edges
}
















