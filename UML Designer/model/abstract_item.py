from abc import ABCMeta, abstractmethod
from PySide2 import QtWidgets
import json


class AbstractItem(metaclass=ABCMeta):
    def __init__(self, name, relationships, function, item_color):
        self.name = name
        self.relationships = relationships
        self.functions = function
        self.item_color = item_color
        self.graphics_item = QtWidgets.QGraphicsPathItem()

    @abstractmethod
    def draw(self, position):
        pass

    def toJSON(self):
        for rel in self.relationships:
            rel.host = rel.host.name
            rel.coordinates = {"x": str(rel.coordinates.x()), "y": rel.coordinates.y()}
        jsonItem = json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                         sort_keys=True, indent=4))
        jsonItem['coordinates'] = {"x": str(self.graphics_item.pos().x()), "y": str(self.graphics_item.pos().y())}
        return json.dumps(jsonItem)
