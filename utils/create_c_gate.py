
def CreateCGate(name, latexname=None):
    """Use a lexical closure to make a controlled gate.
    """
    if not latexname:
        latexname = name
    onequbitgate = CreateOneQubitGate(name, latexname)
    def ControlledGate(ctrls,target):
        return CGate(tuple(ctrls),onequbitgate(target))
    return ControlledGate

