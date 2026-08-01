
def gentitle(name):
    ln = (80 - len(name) - 6) // 2
    return f"/*{ln * '*'} {name} {ln * '*'}*/"

