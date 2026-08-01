
def assert_copy(iter1, iter2, **eql_kwargs) -> None:
    """
    iter1, iter2: iterables that produce elements
    comparable with assert_almost_equal

    Checks that the elements are equal, but not
    the same object. (Does not check that items
    in sequences are also not the same object)
    """
    for elem1, elem2 in zip(iter1, iter2, strict=True):
        assert_almost_equal(elem1, elem2, **eql_kwargs)
        msg = (
            f"Expected object {type(elem1)!r} and object {type(elem2)!r} to be "
            "different objects, but they were the same object."
        )
        assert elem1 is not elem2, msg

