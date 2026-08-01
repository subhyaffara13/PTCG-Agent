
def test_ExprBuilder():
    eb = ExprBuilder(Mul)
    eb.args.extend([x, x])
    assert eb.build() == x**2

