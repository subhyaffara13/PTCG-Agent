
def test_array_interface_excess_dimensions_raises():
    """Regression test for gh-27949.
    Ensure too many dims raises ValueError instead of segfault.
    """

    # Dummy object to hold a custom __array_interface__
    class DummyArray:
        def __init__(self, interface):
            # Attach the array interface dict to mimic an array
            self.__array_interface__ = interface

    # Create a base array (scalar) and copy its interface
    base = np.array(42)  # base can be any scalar or array
    interface = dict(base.__array_interface__)

    # Modify the shape to exceed NumPy's dimension limit (NPY_MAXDIMS, typically 64)
    interface['shape'] = tuple([1] * 136)  # match the original bug report

    dummy = DummyArray(interface)
    # Now, using np.asanyarray on this dummy should trigger a ValueError (not segfault)
    with pytest.raises(ValueError, match="dimensions must be within"):
        np.asanyarray(dummy)

