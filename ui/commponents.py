from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QIntValidator
import sqlite3
conn=sqlite3.connect('database.db')
class PolesComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        cur=conn.cursor()  
        self.addItems([str(i[0]) for i in cur.execute('select id from pole')])
class RangeValidator(QIntValidator):
    def __init__(self, min_value, max_value, parent=None):
        super().__init__(min_value, max_value, parent)
        self.min_value = min_value
        self.max_value = max_value

    def fixup(self, input_text):
        value = int(input_text) if input_text.isdigit() else self.min_value
        value = max(min(value, self.max_value), self.min_value)
        return str(value)