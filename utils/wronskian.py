
def wronskian(functions, var, method='bareiss'):
    """
    Compute Wronskian for [] of functions

    ::

                         | f1       f2        ...   fn      |
                         | f1'      f2'       ...   fn'     |
                         |  .        .        .      .      |
        W(f1, ..., fn) = |  .        .         .     .      |
                         |  .        .          .    .      |
                         |  (n)      (n)            (n)     |
                         | D   (f1) D   (f2)  ...  D   (fn) |

    see: https://en.wikipedia.org/wiki/Wronskian

    See Also
    ========

    sympy.matrices.matrixbase.MatrixBase.jacobian
    hessian
    """

    functions = [sympify(f) for f in functions]
    n = len(functions)
    if n == 0:
        return S.One
    W = Matrix(n, n, lambda i, j: functions[i].diff(var, j))
    return W.det(method)

