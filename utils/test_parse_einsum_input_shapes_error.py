
def test_parse_einsum_input_shapes_error() -> None:
    eq = "ab,bc,cd"
    ops = build_arrays_from_tuples([(2, 3), (3, 4), (4, 5)])

    with pytest.raises(ValueError):
        _ = parse_einsum_input([eq, *ops], shapes=True)

