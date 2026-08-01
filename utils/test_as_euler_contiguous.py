
def test_as_euler_contiguous():
    # The Array API does not specify contiguous arrays, so we can only check for NumPy
    r = Rotation.from_quat([0, 0, 0, 1])
    e1 = r.as_euler('xyz')  # extrinsic euler rotation
    e2 = r.as_euler('XYZ')  # intrinsic
    assert e1.flags['C_CONTIGUOUS'] is True
    assert e2.flags['C_CONTIGUOUS'] is True
    assert all(i >= 0 for i in e1.strides)
    assert all(i >= 0 for i in e2.strides)

