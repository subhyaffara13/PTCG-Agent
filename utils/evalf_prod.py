
def evalf_prod(expr: 'Product', prec: int, options: OPT_DICT) -> TMP_RES:
    if all((l[1] - l[2]).is_Integer for l in expr.limits):
        result = evalf(expr.doit(), prec=prec, options=options)
    else:
        from sympy.concrete.summations import Sum
        result = evalf(expr.rewrite(Sum), prec=prec, options=options)
    return result

