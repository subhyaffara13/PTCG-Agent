
def _a2m_trace(arg):
    if isinstance(arg, _CodegenArrayAbstract):
        return _array_contraction(arg, (0, 1))
    else:
        from sympy.matrices.expressions.trace import Trace
        return Trace(arg)

