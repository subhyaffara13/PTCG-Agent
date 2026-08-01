
def test_too_many_arguments_method_forwarding():
    # Not directly related to the standard argument parsing, but we sometimes
    # forward methods to Python: arr.mean() calls np._core._methods._mean()
    # This adds code coverage for this `npy_forward_method`.
    arr = np.arange(3)
    args = range(1000)
    with pytest.raises(TypeError):
        arr.mean(*args)

