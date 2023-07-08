from PyQt5.QtWidgets import QDialog,QHBoxLayout,QFrame,QVBoxLayout,QLineEdit,QPushButton,QLabel
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QIcon
class LoginPhoto(QFrame):
    def __init__(self,parent):
        super().__init__(parent=parent) 
        self.setObjectName('loginphoto')
        self.frame=QFrame(self)
        self.name,self.disc=QLabel(self.frame,text="OptiRés"),QLabel(self.frame,text="product descriptionproduct descriptionproduct descriptionproduct description")
        self.univ,self.company=QPushButton(self,icon=QIcon("images/usthb.png")),QPushButton(self,icon=QIcon("images/sonelgaz.png"))
        self.univ.setIconSize(QSize(75,75))
        self.company.setIconSize(QSize(75,75))
        self.frame.setObjectName('loginproductframe')
        self.name.setObjectName('loginproductname')
        self.disc.setObjectName('loginproductdisc')
        self.disc.setWordWrap(True)
        self.setLayout()
    def setLayout(self):
        layoutframe,layout,hbox=QVBoxLayout(),QVBoxLayout(),QHBoxLayout()
        hbox.addWidget(self.univ)
        hbox.addWidget(self.company)
        layout.setContentsMargins(0,0,0,0),layout.setSpacing(0)
        layoutframe.setContentsMargins(0,0,0,0),layoutframe.setSpacing(0)
        layoutframe.addWidget(self.name),layoutframe.addWidget(self.disc)
        self.frame.setLayout(layoutframe)
        layout.addWidget(self.frame)
        layout.addStretch(1)
        layout.addLayout(hbox)
        layout.addStretch(1)
        return super().setLayout(layout)
class LoginFrame(QFrame):
    def __init__(self,parent):
        super().__init__(parent=parent)  
        self.setObjectName('loginframe') 
        self.user,self.password, self.btnlogin,self.title=QLineEdit(self),QLineEdit(self),QPushButton(self,text="Log In"),QLabel(self,text="Log In")
        [i[0].setObjectName(i[1]) for i in [[self.btnlogin,"loginbutton"],[self.title,"logintitle"]]]
        self.setFixedWidth(200)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("password")
        self.user.setPlaceholderText("username")
        self.user.returnPressed.connect(self.password.setFocus)
        self.setLayout()
    def setLayout(self):
        layout=QVBoxLayout()
        layout.addStretch(1)
        [layout.addWidget(i) for i in [self.title,self.user,self.password,self.btnlogin]]
        layout.addStretch(1)
        return super().setLayout(layout)
class LogIn(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setObjectName('Login')
        self.setWindowIcon(QIcon('Icon.ico'))
        self.setWindowTitle("Login")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.frame,self.image,self.exit=LoginFrame(self),LoginPhoto(self),QPushButton(self,icon=QIcon("images/close.png"))
        self.exit.setObjectName("close")
        self.exit.setGeometry(self.height()-130,0,50,50)
        self.setLayout()
    def setLayout(self) :
        layout=QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0),layout.setSpacing(0)
        layout.addWidget(self.image),layout.addWidget(self.frame)
        return super().setLayout(layout)
