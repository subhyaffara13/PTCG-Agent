
def test_wrap_radians(xp):
    x = xp.asarray([-math.pi-1, -math.pi, -1, -1e-300,
                    0, 1e-300, 1, math.pi, math.pi+1])
    ref = xp.asarray([math.pi-1, math.pi, -1, -1e-300,
                    0, 1e-300, 1, math.pi, -math.pi+1])
    res = _wrap_radians(x, xp=xp)
    xp_assert_close(res, ref, atol=0)

