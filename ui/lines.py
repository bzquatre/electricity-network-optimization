

from PyQt5.QtWidgets import QApplication , QMessageBox,QWidget,QFormLayout,QHBoxLayout,QLineEdit,QPushButton,QTableWidget,QVBoxLayout,QLabel,QTableWidgetItem,QCompleter
from PyQt5.QtGui import QIcon,QIntValidator
from .commponents import PolesComboBox
from PyQt5.QtCore import Qt
import sqlite3,sys
conn=sqlite3.connect('database.db')
class QLine(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("New line")
        self.setWindowIcon(QIcon('Icon.ico'))
        self.id,self.from_pole,self.to_pole=QLineEdit(self),PolesComboBox(self),PolesComboBox(self)
        self.investment_cost=QLineEdit(self)
        self.flow_cost=QLineEdit(self)
        self.init_resistance=QLineEdit(self)
        self.max_resistance=QLineEdit(self)
        self.length=QLineEdit(self)
        self.id.setDisabled(True)
        self.investment_cost.setValidator(QIntValidator())
        self.flow_cost.setValidator(QIntValidator())
        self.init_resistance.setValidator(QIntValidator())
        self.max_resistance.setValidator(QIntValidator())
        self.length.setValidator(QIntValidator())
        self.validate=QPushButton('validate',self)
        self.validate.clicked.connect(self.addLine)
        self.setLayout()
        self.setMinimumSize(500,400)
    def addLine(self):
        cur=conn.cursor() 
        
        if self.validate.text()=='validate':
            try:
                cur.execute(f"""insert into line  ( "from_pole", "to_pole", "investment_cost", "flow_cost", "init_resistance", "max_resistance", "length")
                            values({self.from_pole.currentText()},{self.to_pole.currentText()},
                            {self.investment_cost.text()},{self.flow_cost.text()},
                            {self.init_resistance.text()},{self.max_resistance.text()},
                            {self.length.text()})""")
                conn.commit()
            except:
                QMessageBox.critical(self, "Line", "Add Line Error")
            else:
                QMessageBox.about(self, "Line", "Add Line Success")
        else:
            try:
                code=int(self.id.text())
                cur.execute(f"""update  line set investment_cost={self.investment_cost.text()},flow_cost={self.flow_cost.text()},
                            init_resistance={self.init_resistance.text()},max_resistance={self.max_resistance.text()},
                            length={self.length.text()} where line_id={code}""")
            except:
                QMessageBox.critical(self, "Line", "Update Line Error ")
            else:
                QMessageBox.about(self, "Line", "Update Line Success")
        self.close()
    def setLayout(self):
        a0,F,h2=QVBoxLayout(),QFormLayout(),QHBoxLayout()
        list(map(lambda i: F.addRow(i[0], i[1]), [['Id Line', self.id],['From', self.from_pole],['TO', self.to_pole],
                            ["investment_cost",self.investment_cost],["flow_cost",self.flow_cost],
                            ["init_resistance",self.init_resistance],["max_resistance",self.max_resistance],
                            ["length",self.length]]))
        h2.addStretch(),h2.addWidget(self.validate)
        a0.addLayout(F),a0.addLayout(h2)
        return super().setLayout(a0)
class QLines(QWidget):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.research,self.add,self.table=QLineEdit(self),QPushButton('insert',self),QTableWidget(self)
        self.add.clicked.connect(self.newLine)
        self.research.setPlaceholderText('research')
        self.initTable()
        self.initResearch()
        self.setLayout()
    def clickedTable(self,row,column):
        cur=conn.cursor()
        if column==self.table.columnCount()-2:
            def close(a0):
                self.initResearch(),self.initTable()
            self.line=QLine()
            self.line.id.setText(str(row[0]))
            self.line.from_pole.setCurrentText(str(row[1]))
            self.line.to_pole.setCurrentText(str(row[2]))
            self.line.investment_cost.setText(str(row[3]))
            self.line.flow_cost.setText(str(row[4]))
            self.line.init_resistance.setText(str(row[5]))
            self.line.max_resistance.setText(str(row[6]))
            self.line.length.setText(str(row[7]))
            self.line.validate.setText('update')
            self.line.show()
            self.line.closeEvent=close
        elif column==self.table.columnCount()-1:
            if QMessageBox.question(self,'Line','Are you sure you want to delete?',QMessageBox.Yes,QMessageBox.No)==QMessageBox.Yes:
                try:
                    cur.execute(f'delete from line  where line_id={row[0]}')
                    conn.commit(),self.initResearch(),self.initTable()
                except:
                    QMessageBox.critical(self, "Line", "erreur")
                else:
                    QMessageBox.about(self, "Line", "success")

    def newLine(self):
        def close(a0):
            self.initResearch(),self.initTable()
        self.product=QLine()
        self.product.show()
        self.product.closeEvent=close
    def initResearch(self):
        cur=conn.cursor()  
        self.completer=QCompleter([str(i[0]) for i in cur.execute('select line_id from line')])
        self.completer.setCaseSensitivity(Qt.CaseInsensitive),self.research.setCompleter(self.completer),self.research.returnPressed.connect(self.initTable)
    def initTable(self,colum=["id Line","from_pole","to_pole","investment_cost","flow_cost","init_resistance","max_resistance","length",'','']):
        cur=conn.cursor()       
        self.table.clear()
        self.table.setColumnCount(len(colum)),
        self.table.setRowCount(0)
        [self.table.setHorizontalHeaderItem(i,QTableWidgetItem(j)) for i,j in enumerate(colum)]
        for row in  cur.execute('select * from line'):
            if self.research.text() in str(row[0]):
                self.table.setRowCount(self.table.rowCount()+1)
                [self.table.setCellWidget(self.table.rowCount()-1,i,QLabel(str(item))) for i,item in enumerate(row)]
                for j,item in enumerate(['delete','update']):
                    self.table.setCellWidget(self.table.rowCount()-1,len(colum)-j-1,QPushButton(item))
                    self.table.cellWidget(self.table.rowCount()-1,len(colum)-j-1).clicked.connect(lambda *args, row=row, column=len(colum)-j-1: self.clickedTable(row, column))
    def setLayout(self):
        v,a0=QHBoxLayout(),QVBoxLayout()
        v.addStretch(),v.addWidget(self.research),v.addWidget(self.add),a0.addWidget(QLabel('Lines')),a0.addWidget(QLabel('lines List')),a0.addLayout(v),a0.addWidget(self.table)
        return super().setLayout(a0)
if __name__=="__main__":
    app=QApplication(sys.argv) 
    app.setStyleSheet(open('style.qss').read())
    mainwindo=QLines(parent=None)
    mainwindo.showMaximized()  
    sys.exit(app.exec_())
