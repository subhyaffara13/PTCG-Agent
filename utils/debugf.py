import sys

def debugf(string, args):
    """
    Print ``string%args`` if SYMPY_DEBUG is True, else do nothing. This is
    intended for debug messages using formatted strings.
    """
    from sympy import SYMPY_DEBUG
    if SYMPY_DEBUG:
        print(string%args, file=sys.stderr)

