import re

def get_abs(expr: Expr, prec: int, options: OPT_DICT) -> TMP_RES:
    result = evalf(expr, prec + 2, options)
    if result is S.ComplexInfinity:
        return finf, None, prec, None
    re, im, re_acc, im_acc = result
    if not re:
        re, re_acc, im, im_acc = im, im_acc, re, re_acc
    if im:
        if expr.is_number:
            abs_expr, _, acc, _ = evalf(abs(N(expr, prec + 2)),
                                        prec + 2, options)
            return abs_expr, None, acc, None
        else:
            if 'subs' in options:
                return libmp.mpc_abs((re, im), prec), None, re_acc, None
            return abs(expr), None, prec, None
    elif re:
        return mpf_abs(re), None, re_acc, None
    else:
        return None, None, None, None

