
def _a2m_add(*args):
    if not any(isinstance(i, _CodegenArrayAbstract) for i in args):
        from sympy.matrices.expressions.matadd import MatAdd
        return MatAdd(*args).doit()
    else:
        return _array_add(*args)

