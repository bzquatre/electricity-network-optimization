

from PyQt5.QtWidgets import QApplication , QMessageBox,QWidget,QFormLayout,QHBoxLayout,QLineEdit,QPushButton,QTableWidget,QVBoxLayout,QLabel,QTableWidgetItem,QCompleter
from PyQt5.QtGui import QIcon,QIntValidator
from PyQt5.QtCore import Qt
import sqlite3,sys
conn=sqlite3.connect('database.db')
class QRequiredEnergy(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("New requiredenergy")
        self.setWindowIcon(QIcon('Icon.ico'))
        self.year,self.energy=QLineEdit(self),QLineEdit(self)
        self.validate=QPushButton('validate',self)
        self.year.setValidator(QIntValidator())
        self.validate.clicked.connect(self.addRequiredEnergy)
        self.setLayout()
        self.setMinimumSize(500,400)
    def addRequiredEnergy(self):
        cur=conn.cursor() 
        if self.validate.text()=='validate':
            try:
                cur.execute(f"insert into requiredenergy (year,energy) values({self.year.text()},'{self.energy.text()}')")
                conn.commit()
            except:
                QMessageBox.critical(self, "RequiredEnergy", "Error")
            else:
                QMessageBox.about(self, "RequiredEnergy", "Success")
        else:
            try:
                code=int(self.year.text())
                cur.execute(f"update  requiredenergy set energy='{self.energy.text()}' where year={code}")
            except:
                QMessageBox.critical(self, "RequiredEnergy", "Error")
            else:
                QMessageBox.about(self, "RequiredEnergy", "Success")
        self.close()
    def setLayout(self):
        a0,F,h2=QVBoxLayout(),QFormLayout(),QHBoxLayout()
        list(map(lambda i: F.addRow(i[0], i[1]), [['Id RequiredEnergy', self.year], ['RequiredEnergy Address', self.energy],]))
        h2.addStretch(),h2.addWidget(self.validate)
        a0.addLayout(F),a0.addLayout(h2)
        return super().setLayout(a0)
class QRequiredEnergys(QWidget):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.research,self.add,self.table=QLineEdit(self),QPushButton('insert',self),QTableWidget(self)
        self.add.clicked.connect(self.newRequiredEnergy)
        self.research.setPlaceholderText('research')
        self.initTable()
        self.initResearch()
        self.setLayout()
    def clickedTable(self,row,column):
        cur=conn.cursor()
        if column==self.table.columnCount()-2:
            def close(a0):
                self.initResearch(),self.initTable()
            self.requiredenergy=QRequiredEnergy()
            self.requiredenergy.year.setText(str(row[0]))
            self.requiredenergy.energy.setText(str(row[1]))
            self.requiredenergy.validate.setText('update')
            self.requiredenergy.show()
            self.requiredenergy.closeEvent=close
        elif column==self.table.columnCount()-1:
            if QMessageBox.question(self,'RequiredEnergy','Are you sure you want to delete?',QMessageBox.Yes,QMessageBox.No)==QMessageBox.Yes:
                try:
                    cur.execute(f'delete from requiredenergy  where year={row[0]}')
                    conn.commit(),self.initResearch(),self.initTable()
                except:
                    QMessageBox.critical(self, "RequiredEnergy", "erreur")
                else:
                    QMessageBox.about(self, "RequiredEnergy", "success")

    def newRequiredEnergy(self):
        def close(a0):
            self.initResearch(),self.initTable()
        self.product=QRequiredEnergy()
        self.product.show()
        self.product.closeEvent=close
    def initResearch(self):
        cur=conn.cursor()  
        self.completer=QCompleter([str(i[0]) for i in cur.execute('select year from requiredenergy')])
        self.completer.setCaseSensitivity(Qt.CaseInsensitive),self.research.setCompleter(self.completer),self.research.returnPressed.connect(self.initTable)
    def initTable(self,colum=['year','Energy','','']):
        cur=conn.cursor()       
        self.table.clear()
        self.table.setColumnCount(len(colum)),
        self.table.setRowCount(0)
        [self.table.setHorizontalHeaderItem(i,QTableWidgetItem(j)) for i,j in enumerate(colum)]
        self.table.setColumnWidth(1,400)
        for row in  cur.execute('select * from requiredenergy'):
            if self.research.text() in str(row[0]):
                self.table.setRowCount(self.table.rowCount()+1)
                [self.table.setCellWidget(self.table.rowCount()-1,i,QLabel(str(item))) for i,item in enumerate(row)]
                for j,item in enumerate(['delete','update']):
                    self.table.setCellWidget(self.table.rowCount()-1,len(colum)-j-1,QPushButton(item))
                    self.table.cellWidget(self.table.rowCount()-1,len(colum)-j-1).clicked.connect(lambda *args, row=row, column=len(colum)-j-1: self.clickedTable(row, column))
    def setLayout(self):
        v,a0=QHBoxLayout(),QVBoxLayout()
        v.addStretch(),v.addWidget(self.research),v.addWidget(self.add),a0.addWidget(QLabel('RequiredEnergys')),a0.addWidget(QLabel('requiredenergys List')),a0.addLayout(v),a0.addWidget(self.table)
        return super().setLayout(a0)
if __name__=="__main__":
    app=QApplication(sys.argv) 
    app.setStyleSheet(open('style.qss').read())
    mainwindo=QRequiredEnergys(parent=None)
    mainwindo.showMaximized()  
    sys.exit(app.exec_())
