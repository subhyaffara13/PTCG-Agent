
def test_vec_of_reference_wrapper():
    """#171: Can't return reference wrappers (or STL structures containing them)"""
    assert (
        str(m.return_vec_of_reference_wrapper(UserType(4)))
        == "[UserType(1), UserType(2), UserType(3), UserType(4)]"
    )

