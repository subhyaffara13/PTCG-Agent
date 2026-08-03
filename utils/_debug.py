import sys

def _debug(text):
    from sympy import SYMPY_DEBUG

    if SYMPY_DEBUG:
        print('-LT- %s%s' % ('  '*_LT_level, text), file=sys.stderr)


def _debug(cmd):
    """
    Render a subprocess command differently depending on DEBUG.
    """
    return cmd if DEBUG else cmd[0]

