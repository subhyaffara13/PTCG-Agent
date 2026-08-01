
def test_brace_initialization():
    """Tests that simple POD classes can be constructed using C++11 brace initialization"""
    a = m.BraceInitialization(123, "test")
    assert a.field1 == 123
    assert a.field2 == "test"

    # Tests that a non-simple class doesn't get brace initialization (if the
    # class defines an initializer_list constructor, in particular, it would
    # win over the expected constructor).
    b = m.NoBraceInitialization([123, 456])
    assert b.vec == [123, 456]

