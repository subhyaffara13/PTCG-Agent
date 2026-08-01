
def test_parse_with_ellisis() -> None:
    eq = "...a,ab"
    shapes = [(2, 3), (3, 4)]
    input_subscripts, output_subscript, operands = parse_einsum_input([eq, *shapes], shapes=True)
    assert input_subscripts == "da,ab"
    assert output_subscript == "db"
    assert shapes == operands

