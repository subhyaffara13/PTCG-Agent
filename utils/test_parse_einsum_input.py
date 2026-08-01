
def test_parse_einsum_input() -> None:
    eq = "ab,bc,cd"
    ops = build_arrays_from_tuples([(2, 3), (3, 4), (4, 5)])
    input_subscripts, output_subscript, operands = parse_einsum_input([eq, *ops])
    assert input_subscripts == eq
    assert output_subscript == "ad"
    assert operands == ops

