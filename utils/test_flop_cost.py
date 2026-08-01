
def test_flop_cost() -> None:
    size_dict = {v: 10 for v in "abcdef"}

    # Loop over an array
    assert 10 == oe.helpers.flop_count("a", False, 1, size_dict)

    # Hadamard product (*)
    assert 10 == oe.helpers.flop_count("a", False, 2, size_dict)
    assert 100 == oe.helpers.flop_count("ab", False, 2, size_dict)

    # Inner product (+, *)
    assert 20 == oe.helpers.flop_count("a", True, 2, size_dict)
    assert 200 == oe.helpers.flop_count("ab", True, 2, size_dict)

    # Inner product x3 (+, *, *)
    assert 30 == oe.helpers.flop_count("a", True, 3, size_dict)

    # GEMM
    assert 2000 == oe.helpers.flop_count("abc", True, 2, size_dict)

