
def test_cpp_callable_cleanup():
    alive_counts = m.test_cpp_callable_cleanup()
    assert alive_counts == [0, 1, 2, 1, 2, 1, 0]

