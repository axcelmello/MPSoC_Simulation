
class Task():
    def __init__(self, program, origin, destiny, load):
        self.program = program # key Prog A
        self.origin = origin   # [x,y]
        self.destiny = destiny # [x,y]
        self.load = load

    def __str__(self):
        return f"Program:{self.program}," \
               f" Origin:{self.origin}," \
               f" Destiny:{self.destiny}."