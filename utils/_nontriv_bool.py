
def _nontrivBool(side):
    return isinstance(side, Boolean) and \
           not isinstance(side, Atom)

