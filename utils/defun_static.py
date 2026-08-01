
def defun_static(f):
    setattr(SpecialFunctions, f.__name__, f)
    return f

