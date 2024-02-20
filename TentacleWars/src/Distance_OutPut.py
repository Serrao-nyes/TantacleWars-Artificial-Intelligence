# from lib.embasp.languages.predicate import Predicate
from TentacleWars.lib.embasp.languages.predicate import Predicate


class Distannce_OutPut(Predicate):
    predicate_name = "Distannce_OutPut"

    def __init__(self, ChainUnits = None):
        Predicate.__init__(self, [("ChainUnits")])
        self.ChainUnits = ChainUnits


    def get_ChainUnits(self):
        return self.ChainUnits

    def set_ChainUnits(self, ChainUnits):
        self.ChainUnits = ChainUnits

    def __str__(self):
        return "Distannce_OutPut(" + str(self.ChainUnits) + ")"