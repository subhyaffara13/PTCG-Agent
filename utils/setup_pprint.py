
def setup_pprint(disable_line_wrap=True):
    from sympy.interactive.printing import init_printing
    from sympy.printing.pretty.pretty import pprint_use_unicode
    import sympy.interactive.printing as interactive_printing
    from sympy.printing.pretty import stringpict

    # Prevent init_printing() in doctests from affecting other doctests
    interactive_printing.NO_GLOBAL = True

    # force pprint to be in ascii mode in doctests
    use_unicode_prev = pprint_use_unicode(False)

    # disable line wrapping for pprint() outputs
    wrap_line_prev = stringpict._GLOBAL_WRAP_LINE
    if disable_line_wrap:
        stringpict._GLOBAL_WRAP_LINE = False

    # hook our nice, hash-stable strprinter
    init_printing(pretty_print=False)

    return use_unicode_prev, wrap_line_prev

