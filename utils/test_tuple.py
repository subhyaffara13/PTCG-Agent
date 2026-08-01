
def test_tuple(doc):
    """std::pair <-> tuple & std::tuple <-> tuple"""
    assert m.pair_passthrough((True, "test")) == ("test", True)
    assert m.tuple_passthrough((True, "test", 5)) == (5, "test", True)
    # Any sequence can be cast to a std::pair or std::tuple
    assert m.pair_passthrough([True, "test"]) == ("test", True)
    assert m.tuple_passthrough([True, "test", 5]) == (5, "test", True)
    assert m.empty_tuple() == ()

    assert (
        doc(m.pair_passthrough)
        == """
        pair_passthrough(arg0: Tuple[bool, str]) -> Tuple[str, bool]

        Return a pair in reversed order
    """
    )
    assert (
        doc(m.tuple_passthrough)
        == """
        tuple_passthrough(arg0: Tuple[bool, str, int]) -> Tuple[int, str, bool]

        Return a triple in reversed order
    """
    )

    assert m.rvalue_pair() == ("rvalue", "rvalue")
    assert m.lvalue_pair() == ("lvalue", "lvalue")
    assert m.rvalue_tuple() == ("rvalue", "rvalue", "rvalue")
    assert m.lvalue_tuple() == ("lvalue", "lvalue", "lvalue")
    assert m.rvalue_nested() == ("rvalue", ("rvalue", ("rvalue", "rvalue")))
    assert m.lvalue_nested() == ("lvalue", ("lvalue", ("lvalue", "lvalue")))

    assert m.int_string_pair() == (2, "items")


def test_tuple():
    assert m.tuple_no_args() == ()
    assert m.tuple_ssize_t() == ()
    assert m.tuple_size_t() == ()
    assert m.get_tuple() == (42, None, "spam")


def test_tuple():
    sT((x,), "(Symbol('x'),)")
    sT((x, y), "(Symbol('x'), Symbol('y'))")


def test_tuple():
    assert str((x,)) == sstr((x,)) == "(x,)"
    assert str((x + y, 1 + x)) == sstr((x + y, 1 + x)) == "(x + y, x + 1)"
    assert str((x + y, (
        1 + x, x**2))) == sstr((x + y, (1 + x, x**2))) == "(x + y, (x + 1, x**2))"

