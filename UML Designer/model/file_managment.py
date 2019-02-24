from PySide2 import QtWidgets, QtCore
import json

from .item_relation import ItemRelation
from .item_interface import ItemInterface
from .item_class import ItemClass
from .item_function import ItemFunction
from .item_atribute import ItemAtribute


class FileManagment():
    @staticmethod
    def save_file(mine_items):
        dlg = QtWidgets.QFileDialog()
        dlg.setWindowTitle('Save file')
        file_name = dlg.getSaveFileName()
        if file_name[0].strip() != "":
            with open(file_name[0], 'w') as file:
                items = []
                for item in mine_items:
                    items.append(item.toJSON())

                file.write(json.dumps(items))

    @staticmethod
    def load_file(path, scene):
        with open(path, 'r') as file:
            mine_items = []
            scene.clear()

            items = json.loads(file.read())
            relations = []

            for i, item in enumerate(items):
                item = json.loads(item)
                if "atributes" in item:
                    new_item = ItemClass(item["name"], [], [], item["item_color"], [])
                else:
                    new_item = ItemInterface(item["name"], [], [], item["item_color"])
                for fun in item["functions"]:
                    new_item.functions.append(ItemFunction(**fun))
                if isinstance(new_item, ItemClass):
                    for atr in item["atributes"]:
                        new_item.atributes.append(ItemAtribute(**atr))
                mine_items.append(new_item)
                new_item.draw(QtCore.QPoint(float(item["coordinates"]['x']), float(item["coordinates"]['y'])))
                scene.addItem(new_item.graphics_item)
                for rel in item["relationships"]:
                    del rel["graphics_item"]
                    relations.append({new_item: ItemRelation(**rel)})

            for rel in relations:
                for key in rel:
                    for item in mine_items:
                        if item.name == rel[key].host:
                            rel[key].host = item
                            rel[key].coordinates = QtCore.QPointF(float(rel[key].coordinates['x']), float(rel[key].coordinates['y']))
                            key.relationships.append(rel[key])
                            scene.addItem(key.relationships[-1].graphics_item)
                            break
            return mine_items
