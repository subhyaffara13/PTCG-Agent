
def sT(expr, string, import_stmt=None, **kwargs):
    """
    sT := sreprTest

    Tests that srepr delivers the expected string and that
    the condition eval(srepr(expr))==expr holds.
    """
    if import_stmt is None:
        ENV2 = ENV
    else:
        ENV2 = ENV.copy()
        exec(import_stmt, ENV2)

    assert srepr(expr, **kwargs) == string
    assert eval(string, ENV2) == expr


def sT(expr, string):
    """
    sT := sreprTest
    from sympy/printing/tests/test_repr.py
    """
    assert srepr(expr) == string
    assert eval(string, ENV) == expr

