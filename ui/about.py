from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout, QWidget,QLabel

from PyQt5.QtCore import Qt
class Title(QLabel):
    def __init__(self,text='',parent=None):
        super().__init__(parent=parent,text=text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
        background:transparent;
        text-align:center;
        font-size: 22px;
        border: none;
        margin:0 100px;        
        """)
class Contains(QLabel):
    def __init__(self,text='',parent=None):
        super().__init__(parent=parent,text=text)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
        background:transparent;
        text-align:center;
        font-size: 14px;
        border: none;
        margin:0 100px;        
        """)
class QAbout(QWidget):
    def __init__(self, parent: QWidget):
        
        super().__init__(parent)
        self.setLayout()
    def setLayout(self):
        a0,h=QHBoxLayout(),QVBoxLayout()
        h.addWidget(Contains("""Knowing the evolution of demand and the topology of the existing distribution network, determine the quantity of electricity flow passing through the transmission lines at different moments during the study period (ten years), in such a way that the sum of discounted costs of investment, transmission, and maintenance is minimized""",self))
        h.addWidget(Title("Creator",self))
        h.addWidget(Contains("""Faculty of Mathematics
Department of Operations Research
MASTER: ERO
Created by:
BOUSBICI Mohamed Amine & KHEMILI Youcef""",self))
        h.addWidget(Title("Algorithms Used",self))
        h.addWidget(Title("Flow Approach",self))
        h.addWidget(Contains("""Firstly, we chose an approach that involves calculating the maximum flow with minimum cost using two algorithms: Preflow Push and Network Simplex.
The purpose of this approach is to find the maximum quantity that the existing network can transmit in order to compare it with the maximum power demand. This comparison allows us to determine whether our current network can support the increase in electricity demand or if it requires reinforcement.""",self))
        h.addWidget(Title("Preflow Push",self))
        h.addWidget(Contains("""The Preflow Push algorithm, also known as the Goldberg-Tarjan algorithm, is one of the most efficient algorithms for calculating a maximum flow in a network. It is sometimes translated into French as the "poussage/réétiquetage" algorithm.""",self))
        h.addWidget(Title("Network Simplex",self))
        h.addWidget(Contains("""The network simplex method is an adaptation of the primal simplex algorithm with bounded variables. The basis is represented as a spanning tree, where variables are represented by arcs, and simplex multipliers are represented by vertex potentials. At each iteration, an entering variable is selected using a pricing strategy.""",self))

        a0.addLayout(h)
        return super().setLayout(a0)
