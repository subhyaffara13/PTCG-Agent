
def _get_wilds(expr):
    return list(expr.atoms(Wild, WildFunction, WildTensor, WildTensorIndex, WildTensorHead))

