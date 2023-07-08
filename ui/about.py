from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout, QWidget,QLabel


class QAbout(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setLayout()
    def setLayout(self):
        a0,h=QHBoxLayout(),QVBoxLayout()
        h.addWidget(QLabel("vkxvdfvodosovsnobnwodnovnosdvsdvonosnodnvsodnonqdvon",self))
        
        h.addWidget(QLabel("vkxvdfvodosovsnobnwodnovnosdvsdvonosnodnvsodnonqdvon",self))
        
        h.addWidget(QLabel("vkxvdfvodosovsnobnwodnovnosdvsdvonosnodnvsodnonqdvon",self))
        
        h.addWidget(QLabel("vkxvdfvodosovsnobnwodnovnosdvsdvonosnodnvsodnonqdvon",self))

        a0.addStretch(1)
        a0.addLayout(h)
        a0.addStretch(1)
        return super().setLayout(a0)
