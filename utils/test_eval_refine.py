
def test_eval_refine():
    class MockExpr(Expr):
        def _eval_refine(self, assumptions):
            return True

    mock_obj = MockExpr()
    assert refine(mock_obj)

