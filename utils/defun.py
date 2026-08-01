
def defun(f):
    setattr(CalculusMethods, f.__name__, f)
    return f


def defun(f):
    SpecialFunctions.defined_functions[f.__name__] = f, False
    return f


def defun(f):
    setattr(Eigen, f.__name__, f)
    return f

