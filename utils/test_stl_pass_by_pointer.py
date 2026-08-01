
def test_stl_pass_by_pointer(msg):
    """Passing nullptr or None to an STL container pointer is not expected to work"""
    with pytest.raises(TypeError) as excinfo:
        m.stl_pass_by_pointer()  # default value is `nullptr`
    assert (
        msg(excinfo.value)
        == """
        stl_pass_by_pointer(): incompatible function arguments. The following argument types are supported:
            1. (v: List[int] = None) -> List[int]

        Invoked with:
    """
    )

    with pytest.raises(TypeError) as excinfo:
        m.stl_pass_by_pointer(None)
    assert (
        msg(excinfo.value)
        == """
        stl_pass_by_pointer(): incompatible function arguments. The following argument types are supported:
            1. (v: List[int] = None) -> List[int]

        Invoked with: None
    """
    )

    assert m.stl_pass_by_pointer([1, 2, 3]) == [1, 2, 3]

