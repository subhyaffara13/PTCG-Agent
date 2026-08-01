
def test_trirefine_masked(interpolator):
    # Repeated points means we will have fewer triangles than points, and thus
    # get masking.
    x, y = np.mgrid[:2, :2]
    x = np.repeat(x.flatten(), 2)
    y = np.repeat(y.flatten(), 2)

    z = np.zeros_like(x)
    tri = mtri.Triangulation(x, y)
    refiner = mtri.UniformTriRefiner(tri)
    interp = interpolator(tri, z)
    refiner.refine_field(z, triinterpolator=interp, subdiv=2)

