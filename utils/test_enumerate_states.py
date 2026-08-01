
def test_enumerate_states():
    test = XKet("foo")
    assert enumerate_states(test, 1, 1) == [XKet("foo_1")]
    assert enumerate_states(
        test, [1, 2, 4]) == [XKet("foo_1"), XKet("foo_2"), XKet("foo_4")]

