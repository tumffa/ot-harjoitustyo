from services.translator import Translator
from services.consoleio import ConsoleIO
from servicehandler import ServiceHandler
from repositories.function_repository import FunctionRepository
from repositories.variable_repository import VariableRepository


def main():
    commands = ['exit', 'af', 'av', 'variables', 'functions', 'solve']
    f_repo = FunctionRepository(commands)
    v_repo = VariableRepository(commands)
    translator = Translator(f_repo, v_repo)
    io = ConsoleIO()
    service_handler = ServiceHandler(io, translator)
    service_handler.run()

if __name__ == "__main__":
    main()
