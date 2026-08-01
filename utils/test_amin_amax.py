
def test_amin_amax():
    for am in [amin, amax]:
        assert am(x).array == x
        assert am(x).axis == None
        assert am(x, axis=3).axis == 3
        with raises(ValueError):
            am(x, y, z)

