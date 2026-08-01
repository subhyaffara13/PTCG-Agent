
def test_structured_to_unstructured() -> None:
    a = np.zeros(4, dtype=[("a", "i4"), ("b", "f4,u2"), ("c", "f4", 2)])
    assert_type(rfn.structured_to_unstructured(a), npt.NDArray[Any])

