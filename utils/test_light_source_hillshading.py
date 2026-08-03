import itertools

def test_light_source_hillshading():
    """
    Compare the current hillshading method against one that should be
    mathematically equivalent. Illuminates a cone from a range of angles.
    """

    def alternative_hillshade(azimuth, elev, z):
        illum = _sph2cart(*_azimuth2math(azimuth, elev))
        illum = np.array(illum)

        dy, dx = np.gradient(-z)
        dy = -dy
        dz = np.ones_like(dy)
        normals = np.dstack([dx, dy, dz])
        normals /= np.linalg.norm(normals, axis=2)[..., None]

        intensity = np.tensordot(normals, illum, axes=(2, 0))
        intensity -= intensity.min()
        intensity /= np.ptp(intensity)
        return intensity

    y, x = np.mgrid[5:0:-1, :5]
    z = -np.hypot(x - x.mean(), y - y.mean())

    for az, elev in itertools.product(range(0, 390, 30), range(0, 105, 15)):
        ls = mcolors.LightSource(az, elev)
        h1 = ls.hillshade(z)
        h2 = alternative_hillshade(az, elev, z)
        assert_array_almost_equal(h1, h2)

