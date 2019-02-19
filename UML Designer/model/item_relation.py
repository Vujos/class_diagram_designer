from PySide2 import QtCore, QtGui, QtWidgets
import math


class ItemRelation():
    def __init__(self, cordinates, relation_type, host=None, reverse=False):
        self.cordinates = cordinates
        self.host = host
        self.relation_type = relation_type
        self.graphics_item = QtWidgets.QGraphicsPathItem()
        self.reverse = reverse

        self.graphics_item.setZValue(1)

    def draw(self, position):
        poligon = self.poligon_type(position)

        painter_path = QtGui.QPainterPath()
        painter_path.addPolygon(poligon)
        self.graphics_item.setPath(painter_path)

    def poligon_type(self, position):
        px = position.x()
        py = position.y()

        if self.host is not None:
            x = self.cordinates.x() + self.host.graphics_item.pos().x()
            y = self.cordinates.y() + self.host.graphics_item.pos().y()
        else:
            x = self.cordinates.x()
            y = self.cordinates.y()

        dist = math.hypot(px - x, py - y)

        self.graphics_item.setBrush(QtGui.QBrush(QtGui.QColor("white")))

        if self.reverse:
            px, x = x, px
            py, y = y, py

        if self.relation_type == "Generalization":
            dist = dist - 10
            poligon = QtGui.QPolygon([QtCore.QPoint(x, y), QtCore.QPoint(x + dist, y), QtCore.QPoint(x + dist, y + 10),
                                      QtCore.QPoint(x + 10 + dist, y), QtCore.QPoint(x + dist, y - 10), QtCore.QPoint(x + dist, y + 0)])
        elif self.relation_type == "Composition":
            self.graphics_item.setBrush(QtGui.QBrush(QtGui.QColor("black")))
            poligon = QtGui.QPolygon([QtCore.QPoint(x, y), QtCore.QPoint(x + 10, y - 5), QtCore.QPoint(x + 20, y),
                                      QtCore.QPoint(x + 10, y + 5), QtCore.QPoint(x, y), QtCore.QPoint(x + dist, y)])
        elif self.relation_type == "Aggregation":
            poligon = QtGui.QPolygon([QtCore.QPoint(x, y), QtCore.QPoint(x - 10, y + 5), QtCore.QPoint(x - 20, y),
                                      QtCore.QPoint(x - 10, y - 5), QtCore.QPoint(x, y), QtCore.QPoint(x + dist, y)])

        self.graphics_item.setRotation(math.degrees(math.atan2(py - y, px - x)))
        self.graphics_item.setTransformOriginPoint(x, y)

        return poligon

    def __str__(self):
        return "Host: {} Relation type: {}".format(self.host.name, self.relation_type)
