
def test_unpack_to_numpy_from_torch():
    """
    Test that torch tensors are converted to NumPy arrays.

    We don't want to create a dependency on torch in the test suite, so we mock it.
    """
    class Tensor:
        def __init__(self, data):
            self.data = data

        def __array__(self):
            return self.data

    torch = ModuleType('torch')
    torch.Tensor = Tensor
    sys.modules['torch'] = torch

    data = np.arange(10)
    torch_tensor = torch.Tensor(data)

    result = cbook._unpack_to_numpy(torch_tensor)
    assert isinstance(result, np.ndarray)
    # compare results, do not check for identity: the latter would fail
    # if not mocked, and the implementation does not guarantee it
    # is the same Python object, just the same values.
    assert_array_equal(result, data)

