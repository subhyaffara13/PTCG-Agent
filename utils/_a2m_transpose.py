
def _a2m_transpose(arg):
    if isinstance(arg, _CodegenArrayAbstract):
        return _permute_dims(arg, [1, 0])
    else:
        from sympy.matrices.expressions.transpose import Transpose
        return Transpose(arg).doit()

