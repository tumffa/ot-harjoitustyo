from services.translator import Translator
from services.consoleio import ConsoleIO
from servicehandler import ServiceHandler


def main():
    translator = Translator()
    io = ConsoleIO()
    service_handler = ServiceHandler(io, translator)
    service_handler.run()


if __name__ == "__main__":
    main()
