
def test_print_floor():
    expr = floor(x)
    assert mathml(expr, printer='presentation') == \
        '<mrow><mo>&#8970;</mo><mi>x</mi><mo>&#8971;</mo></mrow>'

