
def test_shapes():

    def spl_interp(x, y, axis):
        return make_interp_spline(x, y, axis=axis)

    for ip in [KroghInterpolator, BarycentricInterpolator, CubicHermiteSpline,
               pchip, Akima1DInterpolator, CubicSpline, spl_interp]:
        for s1 in SHAPES:
            for s2 in SHAPES:
                for axis in range(-len(s2), len(s2)):
                    if ip != CubicSpline:
                        check_shape(ip, s1, s2, None, axis)
                    else:
                        for bc in ['natural', 'clamped']:
                            extra = {'bc_type': bc}
                            check_shape(ip, s1, s2, None, axis, extra)

