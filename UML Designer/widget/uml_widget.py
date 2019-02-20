from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial

from .item_dialog import ItemForm
from ..model.item_relation import ItemRelation
from ..model.file_managment import FileManagment


class UmlWidget(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(UmlWidget, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)

        self.mine_items = []
        self.ctrl = False
        self.hovered = None
        self.position = None
        self.new_rel = None

        self.setStyleSheet("background-color: #F5F5F5")
        self.add_actions()

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.setScene(self.scene)
        self.setMouseTracking(True)

        self.graphics_item = None

    def moving(self):
        for item in self.mine_items:
            for rel in item.relationships:
                if rel.host.name == self.hovered.name:
                    for hov_rel in self.hovered.relationships:
                        if item.name == hov_rel.host.name and rel.relation_type == hov_rel.relation_type:
                            hov_rel.draw(self.hovered.graphics_item.pos() + rel.cordinates)
                            rel.draw(hov_rel.cordinates + item.graphics_item.pos())

    def relation_exist(self, item):
        for hov_rel in self.hovered.relationships:
            if hov_rel.host.name == item.name:
                for i in range(len(item.relationships) - 1):
                    if item.relationships[i].relation_type == self.new_rel:
                        return True
        return False

    def save_relation(self):
        first_item = self.hovered
        self.scene.removeItem(first_item.relationships[-1].graphics_item)
        self.hovered = self.find_item()
        if self.hovered is not None and not self.relation_exist(first_item):
            self.scene.addItem(first_item.relationships[-1].graphics_item)
            first_item.relationships[-1].host = self.hovered
            first_item.relationships[-1].reverse = True
            self.hovered.relationships.append(ItemRelation(first_item.relationships[-1].cordinates - first_item.graphics_item.pos(),
                                                           self.new_rel, first_item, False))
            first_item.relationships[-1].cordinates = self.position - self.hovered.graphics_item.pos()
            self.scene.addItem(self.hovered.relationships[-1].graphics_item)
        else:
            del first_item.relationships[-1]
        self.new_rel = None
        self.hovered = None

    def hide_actions(self):
        if self.hovered is not None:
            for action in self.actions():
                action.setVisible(True)
            self.hovered.graphics_item.setSelected(True)
        else:
            for action in self.actions():
                if action.text() != "Save to file":
                    action.setVisible(False)

    def add_rel(self, relation_type):
        self.new_rel = relation_type
        self.hovered = self.find_item()
        self.hovered.relationships.append(ItemRelation(self.position, relation_type))
        self.hovered.relationships[-1].draw(self.position)
        self.scene.addItem(self.hovered.relationships[-1].graphics_item)
        self.hovered.graphics_item.setSelected(False)

    def update_rel(self, new_item, old_name):
        for rel in new_item.relationships:
            for item in self.mine_items:
                for item_rel in item.relationships:
                    if item_rel.host.name == old_name:
                        item_rel.host = new_item
                        break

    def add_item(self):
        hovered = self.find_item()
        item_form = ItemForm(self, self.mine_items, hovered)
        if hovered is not None:
            temp_name = hovered.name
            hovered.name = ""
        item_form.exec_()
        if item_form.result() == 1:
            self.mine_items.append(item_form.item)
            if hovered is not None:
                self.position = hovered.graphics_item.pos()
                self.update_rel(item_form.item, hovered.name)
                for hov_rel in hovered.relationships:
                    if hov_rel not in item_form.item.relationships:
                        for rel in hov_rel.host.relationships:
                            if hov_rel.relation_type == rel.relation_type and item_form.item.name == rel.host.name:
                                self.scene.removeItem(rel.graphics_item)
                                hov_rel.host.relationships.remove(rel)
                self.remove_item()
                for rel in item_form.item.relationships:
                    self.scene.addItem(rel.graphics_item)
            item_form.item.draw(self.position)
            self.scene.addItem(item_form.item.graphics_item)
        elif hovered is not None:
            hovered.name = temp_name

    def remove_item(self):
        self.hovered = self.find_item()
        if self.hovered is not None:
            for item in self.mine_items:
                for rel in item.relationships:
                    if rel.host.name == self.hovered.name:
                        self.scene.removeItem(rel.graphics_item)
                        item.relationships.remove(rel)
            for item in self.mine_items:
                if item.graphics_item == self.hovered.graphics_item:
                    self.scene.removeItem(item.graphics_item)
                    for i, rel in enumerate(item.relationships, 0):
                        self.scene.removeItem(rel.graphics_item)
                    self.mine_items.remove(item)
            self.hovered = None

    def find_item(self):
        if self.scene.itemAt(self.position, QtGui.QTransform()) is not None:
            for item in self.mine_items:
                if item.graphics_item == self.scene.itemAt(self.position, QtGui.QTransform()):
                    return item
                elif item.graphics_item == self.scene.itemAt(self.position, QtGui.QTransform()).topLevelItem():
                    return item
        return None

    def add_actions(self):
        remove_item = QtWidgets.QAction(self)
        remove_item.setText("Remove item")
        remove_item.triggered.connect(self.remove_item)
        self.addAction(remove_item)

        generalization = QtWidgets.QAction(self)
        generalization.setText("Generalization")
        generalization.triggered.connect(partial(self.add_rel, "Generalization"))
        self.addAction(generalization)

        Composition = QtWidgets.QAction(self)
        Composition.setText("Composition")
        Composition.triggered.connect(partial(self.add_rel, "Composition"))
        self.addAction(Composition)

        Aggregation = QtWidgets.QAction(self)
        Aggregation.setText("Aggregation")
        Aggregation.triggered.connect(partial(self.add_rel, "Aggregation"))
        self.addAction(Aggregation)

        save_action = QtWidgets.QAction(self)
        save_action.setText("Save to file")
        save_action.triggered.connect(partial(FileManagment.save_file, self.mine_items))
        self.addAction(save_action)

    def mouseMoveEvent(self, event):
        super(UmlWidget, self).mouseMoveEvent(event)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.position = self.mapToScene(event.pos())
        if self.hovered is not None:
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.position = self.mapToScene(event.pos())
            if len(self.scene.selectedItems()) == 0:
                self.hovered.relationships[-1].draw(self.position)
            else:
                self.moving()

    def mousePressEvent(self, event):
        super(UmlWidget, self).mousePressEvent(event)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.position = self.mapToScene(event.pos())
        if self.new_rel is not None:
            self.save_relation()
        self.hovered = self.find_item()
        if event.buttons() & QtCore.Qt.RightButton:
            self.hide_actions()

    def mouseDoubleClickEvent(self, event):
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.position = self.mapToScene(event.pos())
        self.add_item()

    def mouseReleaseEvent(self, event):
        super(UmlWidget, self).mouseReleaseEvent(event)
        if len(self.scene.selectedItems()) > 0:
            self.hovered = None

    def keyPressEvent(self, event):
        super(UmlWidget, self).keyPressEvent(event)
        if event.key() == 16777249:
            self.ctrl = True

    def keyReleaseEvent(self, event):
        super(UmlWidget, self).keyReleaseEvent(event)
        if event.key() == 16777249:
            self.ctrl = False

    def wheelEvent(self, event):
        super(UmlWidget, self).wheelEvent(event)
        if self.ctrl:
            zoomInFactor = 1.25
            zoomOutFactor = 1 / zoomInFactor
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
            oldPos = self.mapToScene(event.pos())
            if event.delta() > 0:
                zoomFactor = zoomInFactor
            else:
                zoomFactor = zoomOutFactor
            self.scale(zoomFactor, zoomFactor)
            newPos = self.mapToScene(event.pos())
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                fname = str(url.toLocalFile())

            self.mine_items = FileManagment.load_file(fname, self.scene)
            for item in self.mine_items:
                self.hovered = item
                self.moving()
            self.hovered = None

        else:
            event.ignore()
