class Translator:
    def calculate(self, string):
        string = string.replace("^", "**")
        if any(character.isalpha() for character in string):
            return False
        try:
            result = eval(string)
        except:
            return False
        return result