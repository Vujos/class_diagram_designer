from plugin_framework.plugin import Plugin
from .widget.uml_widget import UmlWidget


class Main(Plugin):
    def __init__(self, plugin_specification):
        super().__init__(plugin_specification)

    def activate(self):
        print("UML Designer activated")
        # ovde inicijalizuj Device, Broadcaster, Setup klasu i sta sve treba
        # self.setup = Setup()
        # da bi njihovim metodama mogla da pristupas preko widgeta i menjas sta treba preko gui
        # drzi se dijagrama klasa!!!

    def deactivate(self):
        print("UML Designer deactivated")

    def get_widget(self, parent=None):
        print("Viewing UML Designer")
        return UmlWidget(parent), None, None
