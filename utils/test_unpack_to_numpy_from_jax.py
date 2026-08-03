import sys

def test_unpack_to_numpy_from_jax():
    """
    Test that jax arrays are converted to NumPy arrays.

    We don't want to create a dependency on jax in the test suite, so we mock it.
    """
    class Array:
        def __init__(self, data):
            self.data = data

        def __array__(self):
            return self.data

    jax = ModuleType('jax')
    jax.Array = Array

    sys.modules['jax'] = jax

    data = np.arange(10)
    jax_array = jax.Array(data)

    result = cbook._unpack_to_numpy(jax_array)
    assert isinstance(result, np.ndarray)
    # compare results, do not check for identity: the latter would fail
    # if not mocked, and the implementation does not guarantee it
    # is the same Python object, just the same values.
    assert_array_equal(result, data)

