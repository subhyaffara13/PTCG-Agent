
def test_bn_not_ok_dtype(fixture, request, disable_bottleneck):
    obj = request.getfixturevalue(fixture)
    assert not nanops._bn_ok_dtype(obj.dtype, "test")

