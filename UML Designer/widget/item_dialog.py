from PySide2 import QtWidgets
from functools import partial
import re

from ..model.item_interface import ItemInterface
from ..model.item_class import ItemClass
from ..model.item_function import ItemFunction
from ..model.item_atribute import ItemAtribute


class ItemForm(QtWidgets.QDialog):
    def __init__(self, parent, items, item):
        super(ItemForm, self).__init__(parent)
        self.setWindowTitle("Item dialog")
        self.regexAtribute = re.compile(r'(public|private|protected|package|\+|\-|\#|\~)\s*(\w+?)\s*:\s*([a-z,A-Z,_]+)')
        self.regexFunction = re.compile(r'(public|private|protected|package|\+|\-|\#|\~)\s*(static\s)?([a-z,A-Z,_]+?)\s+([a-z,A-Z,_]+?)\s*((\(\s*\))$|(\(([a-z,A-Z,_]+\s+[a-z,A-Z,_]+\s*,\s*){0,}([a-z,A-Z,_]+\s+[a-z,A-Z,_]+){1}\)$))')

        self.item_type = QtWidgets.QComboBox()
        self.name = QtWidgets.QLineEdit()
        self.atributes = QtWidgets.QLineEdit()
        self.funckije = QtWidgets.QLineEdit()

        self.items = items
        self.item = item
        self.item_color = "#abc1fc"

        self.btn_confirm = QtWidgets.QPushButton("Confirm")
        self.btn_cancel = QtWidgets.QPushButton("Cancel")
        self.btn_add_function = QtWidgets.QPushButton("Add function")
        self.btn_add_atribute = QtWidgets.QPushButton("Add atribute")
        self.btn_item_color = QtWidgets.QPushButton("Item color")

        self.formLayout = QtWidgets.QFormLayout()
        self.atributes_layout = QtWidgets.QVBoxLayout()
        self.functions_layout = QtWidgets.QVBoxLayout()
        self.relationships_layout = QtWidgets.QVBoxLayout()
        self.color_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()

        self.populate()

        if self.item is not None:
            self.load_item()

        self.setLayout(self.formLayout)

    def populate(self):
        self.btn_confirm.clicked.connect(self.create_item)
        self.btn_confirm.setStyleSheet("color: green")
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_cancel.setStyleSheet("color: blue")
        self.btn_item_color.clicked.connect(partial(self.change_color, "item"))
        self.btn_add_function.clicked.connect(partial(self.add_hbox, "functions_layout"))
        self.btn_add_atribute.clicked.connect(partial(self.add_hbox, "atributes_layout"))
        self.name.textEdited.connect(self.available_name)

        self.item_type.addItems(["Class", "Interface"])
        self.item_type.currentIndexChanged.connect(self.type_changed)

        self.buttons_layout.addWidget(self.btn_confirm)
        self.buttons_layout.addWidget(self.btn_cancel)

        self.color_layout.addWidget(self.btn_item_color)

        self.formLayout.insertRow(0, ("Type: "), self.item_type)
        self.formLayout.insertRow(1, ("Name: "), self.name)
        self.formLayout.insertRow(2, ("Functions: "), self.btn_add_function)
        self.formLayout.insertRow(3, self.functions_layout)
        self.formLayout.insertRow(4, ("Atributes: "), self.btn_add_atribute)
        self.formLayout.insertRow(5, self.atributes_layout)
        if self.item is not None and len(self.item.relationships) > 0:
            self.formLayout.insertRow(6, QtWidgets.QLabel("Relationships: "))
        self.formLayout.insertRow(7, self.relationships_layout)
        self.formLayout.insertRow(8, self.btn_item_color)
        self.formLayout.insertRow(9, self.buttons_layout)

    def change_color(self, color):
        colorPicker = QtWidgets.QColorDialog()
        colorPicker.exec_()
        if colorPicker.result() == 1:
            self.item_color = colorPicker.selectedColor().name()
            self.btn_item_color.setStyleSheet("color: " + self.item_color)

    def available_name(self):
        if self.name.text().strip() != "":
            for item in self.items:
                if self.name.text().strip() == item.name:
                    self.name.setStyleSheet("color: red")
                    return False
            self.name.setStyleSheet("color: black")
            return True
        return False

    def check_input(self, lineEdit, regex, text):
        if re.match(regex, text):
            lineEdit.setStyleSheet("color: black")
        else:
            lineEdit.setStyleSheet("color: red")

    def add_hbox(self, layout):
        hbox = QtWidgets.QHBoxLayout()
        remove = QtWidgets.QPushButton("remove")
        remove.clicked.connect(partial(self.remove_hbox, layout, hbox))
        remove.setStyleSheet("color: red")
        hbox.addSpacing(10)
        lineEdit = QtWidgets.QLineEdit()
        if layout == "functions_layout":
            hbox.addWidget(lineEdit)
            lineEdit.setFixedWidth(250)
            lineEdit.setText("+ void example(par type)")
            lineEdit.textEdited.connect(partial(self.check_input, lineEdit, self.regexFunction))
            self.functions_layout.addLayout(hbox)
        elif layout == "atributes_layout":
            hbox.addWidget(lineEdit)
            lineEdit.setFixedWidth(250)
            lineEdit.setText("- example : string")
            lineEdit.textEdited.connect(partial(self.check_input, lineEdit, self.regexAtribute))
            self.atributes_layout.addLayout(hbox)
        else:
            label = QtWidgets.QLabel()
            label.setFixedWidth(250)
            hbox.addWidget(label)
            self.relationships_layout.addLayout(hbox)
        hbox.addWidget(remove)

    def remove_hbox(self, layout, hbox):
        for i in range(hbox.count()):
            if hbox.itemAt(i).widget() is not None:
                hbox.itemAt(i).widget().setVisible(False)
        if layout == "functions_layout":
            self.functions_layout.removeItem(hbox)
        elif layout == "atributes_layout":
            self.atributes_layout.removeItem(hbox)
        else:
            self.relationships_layout.removeItem(hbox)

    def visible(self, to_hide):
        for i in range(self.atributes_layout.count()):
            for k in range(self.atributes_layout.itemAt(i).count()):
                if self.atributes_layout.itemAt(i).itemAt(k).widget() is not None:
                    self.atributes_layout.itemAt(i).itemAt(k).widget().setVisible(to_hide)

    def type_changed(self):
        if self.item_type.currentText() == "Class":
            self.formLayout.insertRow(4, ("Atributes: "), self.btn_add_atribute)
            self.formLayout.insertRow(5, self.atributes_layout)
            self.btn_add_atribute.show()
            self.visible(True)
        else:
            self.visible(False)
            self.formLayout.removeWidget(self.btn_add_atribute)
            self.formLayout.removeItem(self.atributes_layout)
            self.btn_add_atribute.hide()
            self.formLayout.removeRow(4)
            self.formLayout.removeRow(4)

    def load_item(self):
        self.name.setText(self.item.name)
        for i, fun in enumerate(self.item.functions, 0):
            self.add_hbox("functions_layout")
            for k in range(self.functions_layout.itemAt(i).count()):
                if type(self.functions_layout.itemAt(i).itemAt(k).widget()) is QtWidgets.QLineEdit:
                    self.functions_layout.itemAt(i).itemAt(k).widget().setText(str(fun))
        if isinstance(self.item, ItemClass):
            for i, atr in enumerate(self.item.atributes, 0):
                self.add_hbox("atributes_layout")
                for k in range(self.atributes_layout.itemAt(i).count()):
                    if type(self.atributes_layout.itemAt(i).itemAt(k).widget()) is QtWidgets.QLineEdit:
                        self.atributes_layout.itemAt(i).itemAt(k).widget().setText(str(atr))
        else:
            self.item_type.setCurrentIndex(1)
        for i, rel in enumerate(self.item.relationships, 0):
            self.add_hbox("relationships_layout")
            for k in range(self.relationships_layout.itemAt(i).count()):
                if type(self.relationships_layout.itemAt(i).itemAt(k).widget()) is QtWidgets.QLabel:
                    label = self.relationships_layout.itemAt(i).itemAt(k).widget()
                    label.setText(str(rel))
                    width = label.fontMetrics().boundingRect(label.text()).width()
                    if width > 250:
                        label.setFixedWidth(width)
        self.item_color = self.item.item_color
        self.btn_item_color.setStyleSheet("color: " + self.item_color)

    def create_item(self):
        if self.available_name():
            rel = []
            if self.item is not None:
                rel = self.add_relationships(self.item.relationships)
            if self.item_type.currentText() == "Class":
                self.item = ItemClass(self.name.text(), [], [], "blue", [])
            else:
                self.item = ItemInterface(self.name.text(), [], [], "blue",)
            self.add_functions()
            self.item.item_color = self.item_color
            self.item.relationships = rel
            if isinstance(self.item, ItemClass):
                self.add_atributes()
            self.done(1)

    def add_relationships(self, rel):
        relat = []
        for i in range(self.relationships_layout.count()):
            for k in range(self.relationships_layout.itemAt(i).count()):
                if type(self.relationships_layout.itemAt(i).itemAt(k).widget()) is QtWidgets.QLabel:
                    relation = self.relationships_layout.itemAt(i).itemAt(k).widget().text()
                    for curent_rel in rel:
                        if relation == str(curent_rel):
                            relat.append(curent_rel)
                            break
        return relat

    def add_atributes(self):
        atributes = []
        for i in range(self.atributes_layout.count()):
            for k in range(self.atributes_layout.itemAt(i).count()):
                if type(self.atributes_layout.itemAt(i).itemAt(k).widget()) is QtWidgets.QLineEdit:
                    atr = self.atributes_layout.itemAt(i).itemAt(k).widget().text()
                    regatr = re.match(self.regexAtribute, atr)
                    if atr is not None and atr not in atributes:
                        atributes.append(atr)
                        self.item.atributes.append(ItemAtribute(regatr.group(1).strip(), regatr.group(2).strip(), regatr.group(3).strip()))

    def add_functions(self):
        functions = []
        for i in range(self.functions_layout.count()):
            for k in range(self.functions_layout.itemAt(i).count()):
                if type(self.functions_layout.itemAt(i).itemAt(k).widget()) is QtWidgets.QLineEdit:
                    fun = self.functions_layout.itemAt(i).itemAt(k).widget().text()
                    regfun = re.match(self.regexFunction, fun)
                    if regfun is not None and fun not in functions:
                        functions.append(fun)
                        params = {k: v for k, v in (x.split() for x in [i for i in regfun.group(5)[1:-1].split(",") if i.strip() != ""])}
                        self.item.functions.append(ItemFunction(regfun.group(1), True if regfun.group(2) is not None else False,
                                                                regfun.group(3), regfun.group(4), params))

    def cancel(self):
        self.done(0)
