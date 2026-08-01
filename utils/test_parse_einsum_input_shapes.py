
def test_parse_einsum_input_shapes() -> None:
    eq = "ab,bc,cd"
    shapes = [(2, 3), (3, 4), (4, 5)]
    input_subscripts, output_subscript, operands = parse_einsum_input([eq, *shapes], shapes=True)
    assert input_subscripts == eq
    assert output_subscript == "ad"
    assert shapes == operands

