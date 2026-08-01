
def check_loc_scale(distfn, arg, m, v, msg):
    # Make `loc` and `scale` arrays to catch bugs like gh-13580 where
    # `loc` and `scale` arrays improperly broadcast with shapes.
    loc, scale = np.array([10.0, 20.0]), np.array([10.0, 20.0])
    mt, vt = distfn.stats(*arg, loc=loc, scale=scale)
    npt.assert_allclose(m*scale + loc, mt)
    npt.assert_allclose(v*scale*scale, vt)

