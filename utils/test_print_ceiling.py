
def test_print_ceiling():
    expr = ceiling(x)
    assert mathml(expr, printer='presentation') == \
        '<mrow><mo>&#8968;</mo><mi>x</mi><mo>&#8969;</mo></mrow>'

