

from PyQt5.QtWidgets import QApplication , QMessageBox,QWidget,QFormLayout,QHBoxLayout,QLineEdit,QPushButton,QTableWidget,QVBoxLayout,QLabel,QTableWidgetItem,QCompleter
from PyQt5.QtGui import QIcon,QIntValidator
from PyQt5.QtCore import Qt
from .commponents import PolesComboBox
import sqlite3,sys
conn=sqlite3.connect('database.db')
class QResource(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("New resource")
        self.setWindowIcon(QIcon('Icon.ico'))
        self.id,self.name,self.capacity=PolesComboBox(self),QLineEdit(self),QLineEdit(self)
        self.validate=QPushButton('validate',self)
        self.id.setValidator(QIntValidator())
        self.capacity.setValidator(QIntValidator())
        self.validate.clicked.connect(self.addResource)
        self.setLayout()
        self.setMinimumSize(500,400)
    def addResource(self):
        cur=conn.cursor() 
        if self.validate.text()=='validate':
            try:
                cur.execute(f"insert into resource (pole_id,name,capacity) values({self.id.currentText()},'{self.name.text()}','{self.capacity.text()}')")
                conn.commit()
            except:
                QMessageBox.critical(self, "Resource", "Add Resource Error")
            else:
                QMessageBox.about(self, "Resource", "Add Resource Success")
        else:
            try:
                code=int(self.id.currentText())
                cur.execute(f"update  resource set name='{self.name.text()}' ,capacity='{self.capacity.text()}' where pole_id={code}")
            except:
                QMessageBox.critical(self, "Resource", "Update Resource Error ")
            else:
                QMessageBox.about(self, "Resource", "Update Resource Success")
        self.close()
    def setLayout(self):
        a0,F,h2=QVBoxLayout(),QFormLayout(),QHBoxLayout()
        list(map(lambda i: F.addRow(i[0], i[1]), [['Id Pole', self.id], ['Resource Name', self.name],['Resource Capacity', self.capacity]]))
        h2.addStretch(),h2.addWidget(self.validate)
        a0.addLayout(F),a0.addLayout(h2)
        return super().setLayout(a0)
class QResources(QWidget):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.research,self.add,self.table=QLineEdit(self),QPushButton('insert',self),QTableWidget(self)
        self.add.clicked.connect(self.newResource)
        self.research.setPlaceholderText('research')
        self.initTable()
        self.initResearch()
        self.setLayout()
    def clickedTable(self,row,column):
        cur=conn.cursor()
        if column==self.table.columnCount()-2:
            def close(a0):
                self.initResearch(),self.initTable()
            self.resource=QResource()
            self.resource.id.setCurrentText(str(row[0]))
            self.resource.name.setText(str(row[1]))
            self.resource.capacity.setText(str(row[2]))
            self.resource.validate.setText('update')
            self.resource.show()
            self.resource.closeEvent=close
        elif column==self.table.columnCount()-1:
            if QMessageBox.question(self,'Resource','Are you sure you want to delete?',QMessageBox.Yes,QMessageBox.No)==QMessageBox.Yes:
                try:
                    cur.execute(f'delete from resource  where pole_id={row[0]}')
                    conn.commit(),self.initResearch(),self.initTable()
                except:
                    QMessageBox.critical(self, "Resource", "erreur")
                else:
                    QMessageBox.about(self, "Resource", "success")

    def newResource(self):
        def close(a0):
            self.initResearch(),self.initTable()
        self.product=QResource()
        self.product.show()
        self.product.closeEvent=close
    def initResearch(self):
        cur=conn.cursor()  
        self.completer=QCompleter([str(i[0]) for i in cur.execute('select pole_id from resource')])
        self.completer.setCaseSensitivity(Qt.CaseInsensitive),self.research.setCompleter(self.completer),self.research.returnPressed.connect(self.initTable)
    def initTable(self,colum=['id','Name','Capacity','','']):
        cur=conn.cursor()       
        self.table.clear()
        self.table.setColumnCount(len(colum)),
        self.table.setRowCount(0)
        [self.table.setHorizontalHeaderItem(i,QTableWidgetItem(j)) for i,j in enumerate(colum)]
        self.table.setColumnWidth(1,400)
        for row in  cur.execute('select * from resource'):
            if self.research.text() in str(row[0]):
                self.table.setRowCount(self.table.rowCount()+1)
                [self.table.setCellWidget(self.table.rowCount()-1,i,QLabel(str(item))) for i,item in enumerate(row)]
                for j,item in enumerate(['delete','update']):
                    self.table.setCellWidget(self.table.rowCount()-1,len(colum)-j-1,QPushButton(item))
                    self.table.cellWidget(self.table.rowCount()-1,len(colum)-j-1).clicked.connect(lambda *args, row=row, column=len(colum)-j-1: self.clickedTable(row, column))
    def setLayout(self):
        v,a0=QHBoxLayout(),QVBoxLayout()
        v.addStretch(),v.addWidget(self.research),v.addWidget(self.add),a0.addWidget(QLabel('Resources')),a0.addWidget(QLabel('resources List')),a0.addLayout(v),a0.addWidget(self.table)
        return super().setLayout(a0)
if __name__=="__main__":
    app=QApplication(sys.argv) 
    app.setStyleSheet(open('style.qss').read())
    mainwindo=QResources(parent=None)
    mainwindo.showMaximized()  
    sys.exit(app.exec_())
