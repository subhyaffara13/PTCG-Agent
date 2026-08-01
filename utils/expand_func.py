
def expand_func(defn: FuncItem, map: dict[TypeVarId, Type]) -> FuncItem:
    visitor = TypeTransformVisitor(map)
    ret = visitor.node(defn)
    assert isinstance(ret, FuncItem)
    return ret


def expand_func(expr, deep=True):
    """
    Wrapper around expand that only uses the func hint.  See the expand
    docstring for more information.

    Examples
    ========

    >>> from sympy import expand_func, gamma
    >>> from sympy.abc import x
    >>> expand_func(gamma(x + 2))
    x*(x + 1)*gamma(x)

    """
    return sympify(expr).expand(deep=deep, func=True, basic=False,
    log=False, mul=False, power_exp=False, power_base=False, multinomial=False)

