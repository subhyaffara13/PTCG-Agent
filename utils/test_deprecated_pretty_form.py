
def test_deprecated_prettyForm():
    with warns_deprecated_sympy():
        from sympy.printing.pretty.pretty_symbology import xstr
        assert xstr(1) == '1'

    with warns_deprecated_sympy():
        from sympy.printing.pretty.stringpict import prettyForm
        p = prettyForm('s', unicode='s')

    with warns_deprecated_sympy():
        assert p.unicode == p.s == 's'

