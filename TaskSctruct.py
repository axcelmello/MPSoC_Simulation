
class Task():
    def __init__(self, program, origin, destiny, load):
        self.program = program
        self.origin = origin
        self.destiny = destiny
        self.load = load

    def __str__(self):
        return f"Program:{self.program}," \
               f" Origin:{self.origin}," \
               f" Destiny:{self.destiny}," \
               f" Processed!."