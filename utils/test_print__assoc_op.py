
def test_print_AssocOp():
    from sympy.core.operations import AssocOp

    class TestAssocOp(AssocOp):
        identity = 0

    expr = TestAssocOp(1, 2)
    assert mpp.doprint(expr) == \
        '<mrow><mi>testassocop</mi><mn>1</mn><mn>2</mn></mrow>'

