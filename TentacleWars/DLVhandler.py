from lib.embasp.platforms.desktop.desktop_handler import DesktopHandler
from lib.embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from lib.embasp.languages.asp.asp_input_program import ASPInputProgram
from lib.embasp.base.option_descriptor import OptionDescriptor

class DLVhandler:

    def __init__(self):
        # Initializes the handler with empty facts and prepares the ASP environment
        self.fatti = ""
        self.handler = DesktopHandler(DLV2DesktopService("DLV2/./dlv2-linux-64_6"))
        self.programVariable = ASPInputProgram()
        self.programFixed = ASPInputProgram()
        self.programFixed.add_files_path("DLV2/test.asp")  # Set the path to your static ASP program
        self.handler.add_program(self.programFixed)
        self.handler.add_program(self.programVariable)

    def getSoluzione(self):
        # Executes the DLV solver and returns the first answer set
        try:
            answersets = self.handler.start_sync()
            for a in answersets.get_answer_sets():
                return str(a)
        except Exception as e:
            print(f"An error occurred while getting the solution: {e}")
            return None

    def trasferisciInDLV(self):
        # Clears the current variable program and adds the updated facts
        self.programVariable.clear_all()
        self.programVariable.add_program(self.fatti)

    def setFatti(self, int1, int2):
        # Updates the facts to be used in the ASP program
        self.fatti = f"int1({int1}).\nint2({int2})."
