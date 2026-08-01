
def stringToProgram(string):
    if isinstance(string, str):
        string = string.split()
    program = []
    for token in string:
        try:
            token = int(token)
        except ValueError:
            try:
                token = float(token)
            except ValueError:
                pass
        program.append(token)
    return program

