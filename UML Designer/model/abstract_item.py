from PySide2 import QtWidgets
import json


class AbstractItem():
    def __init__(self, name, relationships, function, item_color):
        self.name = name
        self.relationships = relationships
        self.functions = function
        self.item_color = item_color
        self.graphics_item = QtWidgets.QGraphicsPathItem()

    def draw(self, position):
        pass

    def toJSON(self):
        for rel in self.relationships:
            rel.host = rel.host.name
            rel.cordinates = {"x": str(rel.cordinates.x()), "y": rel.cordinates.y()}
        jsonItem = json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                         sort_keys=True, indent=4))
        jsonItem['cordinates'] = {"x": str(self.graphics_item.pos().x()), "y": str(self.graphics_item.pos().y())}
        return json.dumps(jsonItem)
