
def convert_frac(frac):
    diff_op = False
    partial_op = False
    if frac.lower and frac.upper:
        lower_itv = frac.lower.getSourceInterval()
        lower_itv_len = lower_itv[1] - lower_itv[0] + 1
        if (frac.lower.start == frac.lower.stop
                and frac.lower.start.type == LaTeXLexer.DIFFERENTIAL):
            wrt = get_differential_var_str(frac.lower.start.text)
            diff_op = True
        elif (lower_itv_len == 2 and frac.lower.start.type == LaTeXLexer.SYMBOL
              and frac.lower.start.text == '\\partial'
              and (frac.lower.stop.type == LaTeXLexer.LETTER
                   or frac.lower.stop.type == LaTeXLexer.SYMBOL)):
            partial_op = True
            wrt = frac.lower.stop.text
            if frac.lower.stop.type == LaTeXLexer.SYMBOL:
                wrt = wrt[1:]

        if diff_op or partial_op:
            wrt = sympy.Symbol(wrt)
            if (diff_op and frac.upper.start == frac.upper.stop
                    and frac.upper.start.type == LaTeXLexer.LETTER
                    and frac.upper.start.text == 'd'):
                return [wrt]
            elif (partial_op and frac.upper.start == frac.upper.stop
                  and frac.upper.start.type == LaTeXLexer.SYMBOL
                  and frac.upper.start.text == '\\partial'):
                return [wrt]
            upper_text = rule2text(frac.upper)

            expr_top = None
            if diff_op and upper_text.startswith('d'):
                expr_top = parse_latex(upper_text[1:])
            elif partial_op and frac.upper.start.text == '\\partial':
                expr_top = parse_latex(upper_text[len('\\partial'):])
            if expr_top:
                return sympy.Derivative(expr_top, wrt)
    if frac.upper:
        expr_top = convert_expr(frac.upper)
    else:
        expr_top = sympy.Number(frac.upperd.text)
    if frac.lower:
        expr_bot = convert_expr(frac.lower)
    else:
        expr_bot = sympy.Number(frac.lowerd.text)
    inverse_denom = sympy.Pow(expr_bot, -1, evaluate=False)
    if expr_top == 1:
        return inverse_denom
    else:
        return sympy.Mul(expr_top, inverse_denom, evaluate=False)

