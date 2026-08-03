from typing import Tuple

def _derivative_dispatch(expr, *variables, **kwargs):
    from sympy.matrices.matrixbase import MatrixBase
    from sympy.matrices.expressions.matexpr import MatrixExpr
    from sympy.tensor.array import NDimArray
    array_types = (MatrixBase, MatrixExpr, NDimArray, list, tuple, Tuple)
    if isinstance(expr, array_types) or any(isinstance(i[0], array_types) if isinstance(i, (tuple, list, Tuple)) else isinstance(i, array_types) for i in variables):
        from sympy.tensor.array.array_derivatives import ArrayDerivative
        return ArrayDerivative(expr, *variables, **kwargs)
    return Derivative(expr, *variables, **kwargs)

