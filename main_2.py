import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.showing)
        self.pushButton_2.clicked.connect(self.add_item)
        cur = self.con.cursor()
        m_value = cur.execute("Select * from coffee").fetchall()
        self.spinBox.setRange(1, len(m_value[0]) - 1)
        for elem in ["молотый", "в зернах"]:
            self.comboBox.addItem(elem)
        self.comboBox.activated[str].connect(self.on_activated)

    def on_activated(self, text):
        self.chosen = text

    def add_item(self):
        kind = self.lineEdit.text()
        power = self.lineEdit_2.text()
        seeds = self.chosen
        taste = self.lineEdit_3.text()
        price = self.lineEdit_4.text()
        volume = self.lineEdit_5.text()
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        cur = self.con.cursor()
        string = """INSERT INTO coffee(kind, power, instant_or_whole_bean, taste, price, value)
                 VALUES('{}', '{}', '{}', '{}', '{}', '{}')""".format(kind, power, seeds, taste, price, volume)
        cur.execute(string)
        self.con.commit()
        cur = self.con.cursor()
        m_value = cur.execute("Select * from coffee").fetchall()
        self.spinBox.setRange(1, len(m_value[0]))
        self.update()

    def showing(self):
        cur = self.con.cursor()
        result = cur.execute("Select * from coffee WHERE id=?",
                             (self.spinBox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()


app = QApplication(sys.argv)
ex = Coffee()
ex.show()
sys.exit(app.exec_())
