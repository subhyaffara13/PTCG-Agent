
def _indenter(s, n=0):
    """
    Ensures that lines after the first are indented by the specified amount
    """
    split = s.split("\n")
    indent = " "*n
    return ("\n" + indent).join(split)

