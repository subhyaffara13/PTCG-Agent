
def test_O4():
    from sympy.vector import CoordSys3D, Del
    N = CoordSys3D("N")
    delop = Del()
    i, j, k = N.base_vectors()
    x, y, z = N.base_scalars()
    F = i*(x*y*z) + j*((x*y*z)**2) + k*((y**2)*(z**3))
    assert delop.cross(F).doit() == (-2*x**2*y**2*z + 2*y*z**3)*i + x*y*j + (2*x*y**2*z**2 - x*z)*k

