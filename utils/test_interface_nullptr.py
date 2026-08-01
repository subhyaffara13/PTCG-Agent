
def test_interface_nullptr(iface):
    iface.update({"data": (0, True)})

    class ArrayLike:
        __array_interface__ = iface

    arr = np.asarray(ArrayLike())
    # Note, we currently set the base anyway, but we do an allocation
    # (because NumPy doesn't like NULL data pointers everywhere).
    assert arr.shape == iface["shape"]
    assert arr.dtype == np.dtype(iface["typestr"])
    assert arr.base is not None
    assert arr.flags.owndata

