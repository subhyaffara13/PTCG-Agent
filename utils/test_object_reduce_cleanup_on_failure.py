
def test_object_reduce_cleanup_on_failure():
    # Test cleanup, including of the initial value (manually provided or not)
    with pytest.raises(TypeError):
        np.add.reduce([1, 2, None], initial=4)

    with pytest.raises(TypeError):
        np.add.reduce([1, 2, None])

