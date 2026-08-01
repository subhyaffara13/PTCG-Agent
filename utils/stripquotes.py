
def stripquotes(s):
    """Replace explicit quotes in a string.

    >>> from sympy.physics.quantum.qasm import stripquotes
    >>> stripquotes("'S'") == 'S'
    True
    >>> stripquotes('"S"') == 'S'
    True
    >>> stripquotes('S') == 'S'
    True
    """
    s = s.replace('"', '') # Remove second set of quotes?
    s = s.replace("'", '')
    return s

