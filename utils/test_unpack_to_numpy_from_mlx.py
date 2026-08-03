import sys

def test_unpack_to_numpy_from_mlx():
    """
    Test that mlx arrays are converted to NumPy arrays.

    We don't want to create a dependency on mlx in the test suite, so we mock it.
    """
    class Array:
        def __init__(self, data):
            self.data = data

        def __array__(self):
            return self.data

    # mlx is something peculiar
    # class `array` is in `mlx.core`
    mlx_core = ModuleType('mlx.core')
    mlx_core.array = Array

    sys.modules['mlx.core'] = mlx_core

    data = np.arange(10)
    mlx_array = mlx_core.array(data)

    result = cbook._unpack_to_numpy(mlx_array)
    assert isinstance(result, np.ndarray)
    # compare results, do not check for identity: the latter would fail
    # if not mocked, and the implementation does not guarantee it
    # is the same Python object, just the same values.
    assert_array_equal(result, data)

