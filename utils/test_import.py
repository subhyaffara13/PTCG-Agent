
def test_import():
    from sympy.parsing.latex._build_latex_antlr import (
        build_parser,
        check_antlr_version,
        dir_latex_antlr
    )
    # XXX: It would be better to come up with a test for these...
    del build_parser, check_antlr_version, dir_latex_antlr

