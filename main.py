from PyQt5.QtWidgets import QApplication,QMessageBox,QMainWindow,QWidget,QTabWidget,QHBoxLayout,QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ui.poles import QPoles
from ui.customers import QCustomers
from ui.resources import QResources
from ui.requiredenergy import QRequiredEnergys
from ui.calculate import QCalculate
from ui.lines import QLines
from ui.about import QAbout
from ui.login import LogIn
import pandas as pd
import sys,sqlite3,os
conn=sqlite3.connect('database.db')
class QDataWindo(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.tab_widget=QTabWidget(self)
        self.pages=[
                    [QPoles(self),QIcon(''),'Poles'],
                    [QCustomers(self),QIcon(''),'Customers'],
                    [QResources(self),QIcon(''),'Resources'],
                    [QLines(self),QIcon(''),'Lines'],
                    [QRequiredEnergys(self),QIcon(''),'Required Energys']
                    ]
        list(map(lambda i: self.tab_widget.addTab(i[0],i[1],i[2]),self.pages))
        """
        self.pages[3][0].contienentre.valider.clicked.connect(self.refreshData)
        self.pages[4][0].contienentre.valider.clicked.connect(self.refreshData)
        """
        self.setLayout()
    def setLayout(self) :
        a0=QHBoxLayout()
        a0.addWidget(self.tab_widget)
        return super().setLayout(a0)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowIcon(QIcon('Icon.ico'))
        self.setWindowTitle("OptiRés")
        self.setObjectName("main")
        self.setMinimumWidth(700)
        central_widget ,self.login= QWidget(),LogIn()
        self.setCentralWidget(central_widget)
        self.tab_widget = QTabWidget(central_widget)
        self.pages = [ 
            [QAbout(self), QIcon(''), 'About'],
            [QDataWindo(self), QIcon(''), 'Data'],
            [QCalculate(self), QIcon(''), 'Calculate'],
        ]
        self.login.exit.clicked.connect(self.closeLogin)
        self.login.frame.btnlogin.clicked.connect(self.userLogin)
        self.login.show()
        
    def closeLogin(self):
        self.close(),self.login.close()

    def userLogin(self):
        if self.login.frame.user.text()=="Admin" and self.login.frame.password.text()=="USTHB":
            for page in self.pages:
                self.tab_widget.addTab(page[0], page[1], page[2])
            self.setLayout()
            self.login.close()
            mainwindo.showMaximized()
        else : 
            QMessageBox.critical(self, "Error","Password or User Incorect")
    def keyPressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if event.key() == Qt.Key_I and modifiers == Qt.ControlModifier:
            home_directory = os.getenv('HOME')
            fname, _ = QFileDialog.getOpenFileName(self, 'Open Books CSV File', home_directory, 'XLSX files (*.xlsx)')
            if fname != '':
                
                # Iterate over the rows and insert data into the database
                data = pd.read_excel(fname, sheet_name='pole')  # Specify the sheet name
                cur = conn.cursor()
                for query in ["delete from resource;", "delete from line;", "delete from customer;", "delete from requiredenergy;", "delete from pole;"]:
                    cur.execute(query)
                for _, row in data.iterrows():
                    cur.execute(f"INSERT INTO pole (id, address) VALUES ({row['id']}, '{row['address']}')")
                conn.commit()
                
                # Iterate over the rows and insert data into the database
                data = pd.read_excel(fname, sheet_name='customer')  # Specify the sheet name

                for _, row in data.iterrows():
                    cur.execute(f"INSERT INTO customer (pole_id, name,capacity) VALUES ({row['id']}, '{row['name']}', '{row['capacity']}')")
                conn.commit()
                # Iterate over the rows and insert data into the database
                data = pd.read_excel(fname, sheet_name='resource')  # Specify the sheet name

                for _, row in data.iterrows():
                    cur.execute(f"INSERT INTO resource (pole_id, name,capacity) VALUES ({row['id']}, '{row['name']}', '{row['capacity']}')")
                conn.commit()
                # Iterate over the rows and insert data into the database
                data = pd.read_excel(fname, sheet_name='line')  # Specify the sheet name
                for _, row in data.iterrows():
                    cur.execute(f"""insert into line  ( "from_pole", "to_pole", "investment_cost", "flow_cost", "init_resistance", "max_resistance", "length")
                            values({row["from"]},{row["to"]},
                            {row["investment cost"]},{row["flow cost"]},
                            {row["init resistance"]},{row["max resistance"]},
                            {row["length"]})""")
                conn.commit()

                # Iterate over the rows and insert data into the database
                data = pd.read_excel(fname, sheet_name='required')  # Specify the sheet name

                for _, row in data.iterrows():
                    cur.execute(f"INSERT INTO requiredenergy (year, energy) VALUES ({row['year']}, '{row['value']}')")
                conn.commit()
        for i in range(5):
            self.pages[1][0].pages[i][0].initResearch(),self.pages[1][0].pages[i][0].initTable()
    def setLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.tab_widget)
        self.centralWidget().setLayout(layout)
class Application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setApplicationName('OptiRés')
        self.setWindowIcon(QIcon('Icon.ico'))
        self.setApplicationVersion('1.2.0')
        self.setStyleSheet(open('style.qss').read())
if __name__=="__main__":
    app=Application() 
    mainwindo=MainWindow() 
    sys.exit(app.exec_())
