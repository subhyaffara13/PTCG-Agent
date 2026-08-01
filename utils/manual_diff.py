
def manual_diff(f, symbol):
    """Derivative of f in form expected by find_substitutions

    SymPy's derivatives for some trig functions (like cot) are not in a form
    that works well with finding substitutions; this replaces the
    derivatives for those particular forms with something that works better.

    """
    if f.args:
        arg = f.args[0]
        if isinstance(f, tan):
            return arg.diff(symbol) * sec(arg)**2
        elif isinstance(f, cot):
            return -arg.diff(symbol) * csc(arg)**2
        elif isinstance(f, sec):
            return arg.diff(symbol) * sec(arg) * tan(arg)
        elif isinstance(f, csc):
            return -arg.diff(symbol) * csc(arg) * cot(arg)
        elif isinstance(f, Add):
            return sum(manual_diff(arg, symbol) for arg in f.args)
        elif isinstance(f, Mul):
            if len(f.args) == 2 and isinstance(f.args[0], Number):
                return f.args[0] * manual_diff(f.args[1], symbol)
    return f.diff(symbol)

