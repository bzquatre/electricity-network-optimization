

from PyQt5.QtWidgets import QMessageBox,QWidget,QLabel,QHBoxLayout,QLineEdit,QPushButton,QVBoxLayout
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QIntValidator,QRegExpValidator
from pulp import *
import matplotlib.pyplot as plt
import networkx as nx
import sqlite3
conn=sqlite3.connect('database.db')
class Gen():
    def __init__(self):
        cur=conn.cursor()
        edges=[]
        self.cost_inv,self.i_capacity,self.max_capacity,self.cost_flow  = {},{},{},{}
        for i in cur.execute("select from_pole,to_pole,investment_cost,init_resistance,max_resistance,flow_cost from line"):
            edge=(int(i[0]),int(i[1]) )
            edges.append(edge)
            self.cost_inv[edge] = int(i[2])
            self.i_capacity[edge] = int(i[3])
            self.max_capacity[edge] = int(i[4])
            self.cost_flow[edge] = int(i[5])
        self.G = nx.DiGraph(edges)
        pos = nx.spring_layout(self.G)
        self.s = list(set([int(i[0]) for i in cur.execute("select pole_id from resource")]))
        self.p = list(set([int(i[0]) for i in cur.execute("select pole_id from customer")]))
        #nx.draw_networkx_labels(self.G, pos, font_family="sans-serif")
        #nx.draw_networkx_nodes(self.G, pos, nodelist=self.s, node_size=400,node_color="red")
        #nx.draw_networkx_nodes(self.G, pos, nodelist=self.p, node_size=400, node_color="orange")
        self.edges = self.G.edges
        self.nodes = self.G.nodes
        
    def setTemp(self,temp):
        cur=conn.cursor()
        self.T=temp
        self.demand = {j+1: energy for j,energy in enumerate(cur.execute(f"select energy from requiredenergy LIMIT {self.T}"))}

class QCalculate(QWidget):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.gen=Gen()
        self.years=QLineEdit(self)
        self.setObjectName("calculate")
        self.years.setValidator(QIntValidator(1, 100))
        self.years.setMinimumWidth(300)
        #self.years.setPlaceholderText("period c de l'intervalle en années")
        self.cout,self.draw=QPushButton("Cost",self),QPushButton("Draw",self)
        self.cout.clicked.connect(self.calculCout)
        self.draw.clicked.connect(self.drawGraph)
        self.setLayout()
    def drawGraph(self):
        self.gen=Gen()
        self.gen.setTemp(int(self.years.text()))
        pos = nx.spring_layout(self.gen.G)
        nx.draw(self.gen.G, with_labels=pos)
        plt.show()
    def calculCout(self):
        self.gen=Gen()
        self.gen.setTemp(int(self.years.text()))
        QMessageBox.about(self, "Cout total","Cout total :"+str(sum(self.fun_opt(self.gen.T, dicts_only=True)[3])))
    def setLayout(self):
        a0,h,h1,h2=QVBoxLayout(),QHBoxLayout(),QHBoxLayout(),QHBoxLayout()
        h.addStretch(1)
        h.addWidget(self.cout)
        h.addWidget(self.draw)
        h.addStretch(1)
        a0.addStretch(1)

        h2.addStretch(1)
        h2.addWidget(QLabel("period c de l'intervalle en années",self))
        h2.addStretch(1)

        h1.addStretch(1)
        h1.addWidget(self.years)
        h1.addStretch(1)
        a0.addLayout(h2)
        a0.addLayout(h1)
        a0.addLayout(h)
        a0.addStretch(1)
        return super().setLayout(a0)
    def build_graph(self,s, p, nodes, edges):
        n_nodes = []
        n_nodes += nodes
        n_nodes.append(0)
        n_nodes.append(len(nodes)+1)
        n_nodes.sort()
        n_edges = []
        n_edges += edges
        for i in s:
            n_edges.append((0, i))
        for i in p:
            n_edges.append((i, len(nodes)+1))
        n_edges.append((len(nodes)+1,0))
        return n_nodes, n_edges

    def get_actual_cost(self,t, p, unit_cost_dict):
        edges = []
        for k, _ in unit_cost_dict.items():
            edges.append(k)
        t_ind = [i for i in range(t)]
        actual_cost_dict = {
        i: {j: unit_cost_dict[j]/(1+p)**i for j in edges} for i in t_ind
        }

        return actual_cost_dict

    def get_actual_cost_i(self,t, p, unit_cost_dict):
        edges = []
        for k, _ in unit_cost_dict.items():
            edges.append(k)
        actual_cost_dict = {
        j: unit_cost_dict[j]/(1+p)**(t-1) for j in edges
        }

        return actual_cost_dict


    def fun_opt(self,t, dicts_only=False):

        # get new nodes list and new edges list
        n_nodes, n_edges = self.build_graph(self.gen.s, self.gen.p, self.gen.nodes, self.gen.edges)

        # get actual cost
        actual_cost = self.get_actual_cost(t, p=0.05, unit_cost_dict=self.gen.cost_inv)

        # create period list t
        t = [i+1 for i in range(t)]

        # create model
        model = LpProblem("Minimisation_des_coûts_d'investissement", LpMinimize)

        # create indices for decision variables
        t_indices = [0] + t

        # variables de décision
        x = LpVariable.dicts("capacity", (t_indices, self.gen.edges), lowBound=0, cat='Continuous')
        y = LpVariable.dicts("flow", (t, n_edges), lowBound=0, cat='Continuous')

        # objectif function 
        model += lpSum(y[i][j]*self.gen.cost_flow[j] for i in t for j in self.gen.edges) + lpSum(actual_cost[i-1][j]*(x[i][j]-x[i-1][j]) for i in t for j in self.gen.edges)

        # constraints
        # set initial capacity
        for j in self.gen.edges:
            model += x[0][j] == self.gen.i_capacity[j]


        # capacity 
        for j in self.gen.edges:
            model += x[t[-1]][j] <= self.gen.max_capacity[j]


        # equipment size can't decrease
        for i in t:
            for j in self.gen.edges:
                model += x[i][j] >= x[i-1][j]


        # flow conservation
        for i in t:
            for n in n_nodes:
                model += lpSum(y[i][j,n] for j in n_nodes if (j,n) in y[i]) == lpSum(y[i][n,k] for k in n_nodes if (n,k) in y[i])

        # flow capacity
        for i in t:
            for j in self.gen.edges:
                model += y[i][j] <= x[i][j]


        # demand 
        for i in t:
            model += y[i][n_nodes[-1],0] >= self.gen.demand[i]

        # solve the problem
        LpSolverDefault.msg = 0
        model.solve()


        c_list = []
        
        for i in t:
            cost_year = 0
            for j in self.gen.edges:
                cost_year += actual_cost[i-1][j]*(x[i][j].value()-x[i-1][j].value())
                cost_year += y[i][j].value()*self.gen.cost_flow[j]   
            c_list.append(cost_year)

        if dicts_only:
            cap_dict = {
                i: {j: x[i][j].value() for j in self.gen.edges} for i in t
            }
            f_dict = {
                i: {j: y[i][j].value() for j in self.gen.edges} for i in t
            }
            c_dict = {
                i: c_list[i-1] for i in t
            }
            
            return cap_dict, f_dict, c_dict, c_list
        else:
            # afficher le statut de la solution
            print("Statut :", LpStatus[model.status])

            # afficher la valeur de flot pour toute la période d'étude
            for v in model.variables():
                print(v.name, "=", v.varValue)       
            
            for i in t:
                print(f"Coût optimal pour l'année {i} = {c_list[i-1]}")
            
            print(f"Coût optimal pour une durée de {t[-1]} ans = {sum(c_list)}")


    

