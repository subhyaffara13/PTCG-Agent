
def pretty(expr):
    """ASCII pretty-printing"""
    return xpretty(expr, use_unicode=False, wrap_line=False)


def pretty(expr, **settings):
    """Returns a string containing the prettified form of expr.

    For information on keyword arguments see pretty_print function.

    """
    pp = PrettyPrinter(settings)

    # XXX: this is an ugly hack, but at least it works
    use_unicode = pp._settings['use_unicode']
    uflag = pretty_use_unicode(use_unicode)

    try:
        return pp.doprint(expr)
    finally:
        pretty_use_unicode(uflag)


def pretty(expr, order=None):
    """ASCII pretty-printing"""
    return xpretty(expr, order=order, use_unicode=False, wrap_line=False)


def pretty(expr):
    """ASCII pretty-printing"""
    return xpretty(expr, use_unicode=False, wrap_line=False)

