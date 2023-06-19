

from PyQt5.QtWidgets import QApplication,QFileDialog , QMessageBox,QWidget,QFormLayout,QHBoxLayout,QLineEdit,QPushButton,QTableWidget,QVBoxLayout,QLabel,QTableWidgetItem,QCompleter
from PyQt5.QtGui import QIcon,QIntValidator
from PyQt5.QtCore import Qt
import pandas as pd
import sqlite3,sys,os
conn=sqlite3.connect('database.db')
class QPole(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("New pole")
        self.setWindowIcon(QIcon('Icon.ico'))
        self.id,self.address=QLineEdit(self),QLineEdit(self)
        self.validate=QPushButton('validate',self)
        self.id.setValidator(QIntValidator())
        self.validate.clicked.connect(self.addPole)
        self.setLayout()
        self.setMinimumSize(500,400)
    def addPole(self):
        cur=conn.cursor() 
        if self.validate.text()=='validate':
            try:
                cur.execute(f"insert into pole (id,address) values({self.id.text()},'{self.address.text()}')")
                conn.commit()
            except:
                QMessageBox.critical(self, "Pole", "Error")
            else:
                QMessageBox.about(self, "Pole", "Success")
        else:
            try:
                code=int(self.id.text())
                cur.execute(f"update  pole set address='{self.address.text()}' where id={code}")
            except:
                QMessageBox.critical(self, "Pole", "Error")
            else:
                QMessageBox.about(self, "Pole", "Success")
        self.close()
    def setLayout(self):
        a0,F,h2=QVBoxLayout(),QFormLayout(),QHBoxLayout()
        list(map(lambda i: F.addRow(i[0], i[1]), [['Id Pole', self.id], ['Pole Address', self.address],]))
        h2.addStretch(),h2.addWidget(self.validate)
        a0.addLayout(F),a0.addLayout(h2)
        return super().setLayout(a0)
class QPoles(QWidget):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.research,self.add,self.table=QLineEdit(self),QPushButton('insert',self),QTableWidget(self)
        self.add.clicked.connect(self.newPole)
        self.research.setPlaceholderText('research')
        self.initTable()
        self.initResearch()
        self.setLayout()
    def clickedTable(self,row,column):
        cur=conn.cursor()
        if column==self.table.columnCount()-2:
            def close(a0):
                self.initResearch(),self.initTable()
            self.pole=QPole()
            self.pole.id.setText(str(row[0]))
            self.pole.address.setText(str(row[1]))
            self.pole.validate.setText('update')
            self.pole.show()
            self.pole.closeEvent=close
        elif column==self.table.columnCount()-1:
            if QMessageBox.question(self,'Pole','Are you sure you want to delete?',QMessageBox.Yes,QMessageBox.No)==QMessageBox.Yes:
                try:
                    cur.execute(f'delete from pole  where id={row[0]}')
                    conn.commit(),self.initResearch(),self.initTable()
                except:
                    QMessageBox.critical(self, "Pole", "erreur")
                else:
                    QMessageBox.about(self, "Pole", "success")

    def newPole(self):
        def close(a0):
            self.initResearch(),self.initTable()
        self.product=QPole()
        self.product.show()
        self.product.closeEvent=close
    def initResearch(self):
        cur=conn.cursor()  
        self.completer=QCompleter([str(i[0]) for i in cur.execute('select id from pole')])
        self.completer.setCaseSensitivity(Qt.CaseInsensitive),self.research.setCompleter(self.completer),self.research.returnPressed.connect(self.initTable)
    def initTable(self,colum=['id','Address','','']):
        cur=conn.cursor()       
        self.table.clear()
        self.table.setColumnCount(len(colum)),
        self.table.setRowCount(0)
        [self.table.setHorizontalHeaderItem(i,QTableWidgetItem(j)) for i,j in enumerate(colum)]
        self.table.setColumnWidth(1,400)
        for row in  cur.execute('select * from pole'):
            if self.research.text() in str(row[0]):
                self.table.setRowCount(self.table.rowCount()+1)
                [self.table.setCellWidget(self.table.rowCount()-1,i,QLabel(str(item))) for i,item in enumerate(row)]
                for j,item in enumerate(['delete','update']):
                    self.table.setCellWidget(self.table.rowCount()-1,len(colum)-j-1,QPushButton(item))
                    self.table.cellWidget(self.table.rowCount()-1,len(colum)-j-1).clicked.connect(lambda *args, row=row, column=len(colum)-j-1: self.clickedTable(row, column))
    def setLayout(self):
        v,a0=QHBoxLayout(),QVBoxLayout()
        v.addStretch(),v.addWidget(self.research),v.addWidget(self.add),a0.addWidget(QLabel('Poles')),a0.addWidget(QLabel('poles List')),a0.addLayout(v),a0.addWidget(self.table)
        return super().setLayout(a0)
    def keyPressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if event.key() == Qt.Key_I and modifiers == Qt.ControlModifier:
            home_directory = os.getenv('HOME')
            fname, _ = QFileDialog.getOpenFileName(self, 'Open Books CSV File ', home_directory, 'XLSX files (*.xlsx)')
            if fname!='':
                data = pd.read_excel(fname)
                # Iterate over the rows and insert data into the database
                cur=conn.cursor()
                for _, row in data.iterrows():
                    cur.execute(f"insert into pole (id,address) values({row['id']},'{row['address']}')"
                    )
                conn.commit()
if __name__=="__main__":
    app=QApplication(sys.argv) 
    app.setStyleSheet(open('style.qss').read())
    mainwindo=QPoles(parent=None)
    mainwindo.showMaximized()  
    sys.exit(app.exec_())
