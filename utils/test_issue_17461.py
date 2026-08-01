
def test_issue_17461():
    class A(Symbol):
        is_extended_real = True

        def _eval_evalf(self, prec):
            return Float(5.0)

    x = A('X')
    y = A('Y')
    assert abs(atan2(x, y).evalf() - 0.785398163397448) <= 1e-10

