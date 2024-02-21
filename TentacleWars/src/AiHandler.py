from TentacleWars.lib.embasp.platforms.desktop.desktop_handler import DesktopHandler
from TentacleWars.lib.embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from TentacleWars.lib.embasp.languages.asp.asp_mapper import ASPMapper
from TentacleWars.lib.embasp.languages.asp.asp_input_program import ASPInputProgram
from TentacleWars.lib.embasp.languages.asp.asp_filter_option import OptionDescriptor
from TentacleWars.lib.embasp.base.callback import Callback
from Cell import Cell_Predicate
from Distance_OutPut import Distannce_OutPut
import platform


class MyCallback(Callback):
    def __init__(self):
        super().__init__()

    def callback(self, answerSets):
        for answerSet in answerSets.get_optimal_answer_sets():
            for obj in answerSet.get_atoms():
                print("ddddddd")
                #print(f"FROM ASP  " + {Distannce_OutPut.get_ChainUnits()})

class AiHandler():
    file_name1 = "ai/Level4.asp"
    #file_name2 = "ai/tetris1.asp"
    to_execute = file_name1
    #mappings = "ai/mappings.asp"
    #if platform.system() == "Darwin":
        #executable_name = "executable/dlv-2.1.1-macos"
    #if platform.system() == "Windows":
        #executable_name = "executable/dlv-2.1.1-windows64.exe"
    executable_name = "/home/giu/PycharmProjects/TantacleWars-Artificial-Intelligence/TentacleWars/executable/dlv-2.1.1-linux-x86_64"
#comm
    def __init__(self):
        self.handler = DesktopHandler(DLV2DesktopService(AiHandler.executable_name))
        ASPMapper.get_instance().register_class(Cell_Predicate)
        ASPMapper.get_instance().register_class(Distannce_OutPut)
        self.fixedProgram = ASPInputProgram()
        self.variableProgram = ASPInputProgram()
        self.handler.add_program(self.fixedProgram)
        self.handler.add_program(self.variableProgram)
        #self.fixedProgram.add_files_path(AiHandler.mappings)
        o = OptionDescriptor("--filter=output/2")
        self.handler.add_option(o)
        self.variableProgram.add_files_path(AiHandler.to_execute)
        c = Cell_Predicate(300,300,0,"red",0,"ATT","Defense",0,False,0,False)
        self.variableProgram.add_object_input(c)
    """
    def changeVariableProgram(self, matrix, currentPiece, nextPiece):
        for i in range(20):
            for j in range(10):
                self.variableProgram.add_object_input(Cell(i, j, matrix[i][j]))
        c = CurrentPiece(currentPiece)
        if nextPiece != None:
            AiHandler.to_execute = AiHandler.file_name1
            n = NextPiece(nextPiece)
            self.variableProgram.add_object_input(n)
        else:
            AiHandler.to_execute = AiHandler.file_name2
        self.variableProgram.add_files_path(AiHandler.to_execute)
        self.variableProgram.add_object_input(c)
    """
    def execute(self): #mainBoard):
        c = MyCallback() #mainBoard
        return self.handler.start_sync([c])

    """
    def clearVariableProgram(self):
        self.variableProgram.clear_all()
    """

