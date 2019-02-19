from .abstract_item import AbstractItem
from PySide2 import QtCore, QtGui, QtWidgets


class ItemClass(AbstractItem):
    def __init__(self, name, relationships, function, item_color, atributes):
        super().__init__(name, relationships, function, item_color)
        self.atributes = atributes

    def draw(self, cordinates):
        painter_path = QtGui.QPainterPath()

        atr_size = len(self.atributes) * 30
        fun_size = len(self.functions) * 30

        atr_size = 30 if atr_size == 0 else atr_size
        fun_size = 30 if fun_size == 0 else fun_size

        itemFont = QtGui.QFont().setPointSize(10)
        textItem = QtWidgets.QGraphicsSimpleTextItem(self.name, self.graphics_item)
        textItem.setFont(itemFont)
        textItem.setPos(5, 10)
        fm = QtGui.QFontMetrics(itemFont)
        width = 100 if fm.width(self.name) < 100 else fm.width(self.name)

        for i, atribute in enumerate(self.atributes, 1):
            textItem = QtWidgets.QGraphicsSimpleTextItem(str(atribute), self.graphics_item)
            textItem.setFont(itemFont)
            textItem.setPos(5, 10 + 30 * i)
            width = fm.width(str(atribute)) if fm.width(str(atribute)) > width else width

        for i, function in enumerate(self.functions, 1):
            textItem = QtWidgets.QGraphicsSimpleTextItem(str(function), self.graphics_item)
            textItem.setFont(itemFont)
            textItem.setPos(5, 10 + atr_size + 30 * i)
            width = fm.width(str(function)) if fm.width(str(function)) > width else width

        width = width + 10
        painter_path.addRect(QtCore.QRect(0, 0, width, 30))
        painter_path.addRect(QtCore.QRect(0, 30, width, atr_size))
        painter_path.addRect(QtCore.QRect(0, 30 + atr_size, width, fun_size))

        self.graphics_item.setBrush(QtGui.QBrush(QtGui.QColor(self.item_color)))
        self.graphics_item.setFlag(QtWidgets.QGraphicsRectItem.ItemIsSelectable)
        self.graphics_item.setFlag(QtWidgets.QGraphicsRectItem.ItemIsMovable)

        self.graphics_item.setPath(painter_path)
        self.graphics_item.setPos(cordinates)

    def __str__(self):
        return "Class\nName: {}\nRelationships: {}\nFunctions: {}\nAtributes: {}".format(self.name, self.relationships, self.functions, self.atributes)
