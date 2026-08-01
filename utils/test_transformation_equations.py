
def test_transformation_equations():

    x, y, z = symbols('x y z')
    # Str
    a = CoordSys3D('a', transformation='spherical',
                   variable_names=["r", "theta", "phi"])
    r, theta, phi = a.base_scalars()

    assert r == a.r
    assert theta == a.theta
    assert phi == a.phi

    raises(AttributeError, lambda: a.x)
    raises(AttributeError, lambda: a.y)
    raises(AttributeError, lambda: a.z)

    assert a.transformation_to_parent() == (
        r*sin(theta)*cos(phi),
        r*sin(theta)*sin(phi),
        r*cos(theta)
    )
    assert a.lame_coefficients() == (1, r, r*sin(theta))
    assert a.transformation_from_parent_function()(x, y, z) == (
        sqrt(x ** 2 + y ** 2 + z ** 2),
        acos((z) / sqrt(x**2 + y**2 + z**2)),
        atan2(y, x)
    )
    a = CoordSys3D('a', transformation='cylindrical',
                   variable_names=["r", "theta", "z"])
    r, theta, z = a.base_scalars()
    assert a.transformation_to_parent() == (
        r*cos(theta),
        r*sin(theta),
        z
    )
    assert a.lame_coefficients() == (1, a.r, 1)
    assert a.transformation_from_parent_function()(x, y, z) == (sqrt(x**2 + y**2),
                            atan2(y, x), z)

    a = CoordSys3D('a', 'cartesian')
    assert a.transformation_to_parent() == (a.x, a.y, a.z)
    assert a.lame_coefficients() == (1, 1, 1)
    assert a.transformation_from_parent_function()(x, y, z) == (x, y, z)

    # Variables and expressions

    # Cartesian with equation tuple:
    x, y, z = symbols('x y z')
    a = CoordSys3D('a', ((x, y, z), (x, y, z)))
    a._calculate_inv_trans_equations()
    assert a.transformation_to_parent() == (a.x1, a.x2, a.x3)
    assert a.lame_coefficients() == (1, 1, 1)
    assert a.transformation_from_parent_function()(x, y, z) == (x, y, z)
    r, theta, z = symbols("r theta z")

    # Cylindrical with equation tuple:
    a = CoordSys3D('a', [(r, theta, z), (r*cos(theta), r*sin(theta), z)],
                   variable_names=["r", "theta", "z"])
    r, theta, z = a.base_scalars()
    assert a.transformation_to_parent() == (
        r*cos(theta), r*sin(theta), z
    )
    assert a.lame_coefficients() == (
        sqrt(sin(theta)**2 + cos(theta)**2),
        sqrt(r**2*sin(theta)**2 + r**2*cos(theta)**2),
        1
    )  # ==> this should simplify to (1, r, 1), tests are too slow with `simplify`.

    # Definitions with `lambda`:

    # Cartesian with `lambda`
    a = CoordSys3D('a', lambda x, y, z: (x, y, z))
    assert a.transformation_to_parent() == (a.x1, a.x2, a.x3)
    assert a.lame_coefficients() == (1, 1, 1)
    a._calculate_inv_trans_equations()
    assert a.transformation_from_parent_function()(x, y, z) == (x, y, z)

    # Spherical with `lambda`
    a = CoordSys3D('a', lambda r, theta, phi: (r*sin(theta)*cos(phi), r*sin(theta)*sin(phi), r*cos(theta)),
                   variable_names=["r", "theta", "phi"])
    r, theta, phi = a.base_scalars()
    assert a.transformation_to_parent() == (
        r*sin(theta)*cos(phi), r*sin(phi)*sin(theta), r*cos(theta)
    )
    assert a.lame_coefficients() == (
        sqrt(sin(phi)**2*sin(theta)**2 + sin(theta)**2*cos(phi)**2 + cos(theta)**2),
        sqrt(r**2*sin(phi)**2*cos(theta)**2 + r**2*sin(theta)**2 + r**2*cos(phi)**2*cos(theta)**2),
        sqrt(r**2*sin(phi)**2*sin(theta)**2 + r**2*sin(theta)**2*cos(phi)**2)
    )  # ==> this should simplify to (1, r, sin(theta)*r), `simplify` is too slow.

    # Cylindrical with `lambda`
    a = CoordSys3D('a', lambda r, theta, z:
        (r*cos(theta), r*sin(theta), z),
        variable_names=["r", "theta", "z"]
    )
    r, theta, z = a.base_scalars()
    assert a.transformation_to_parent() == (r*cos(theta), r*sin(theta), z)
    assert a.lame_coefficients() == (
        sqrt(sin(theta)**2 + cos(theta)**2),
        sqrt(r**2*sin(theta)**2 + r**2*cos(theta)**2),
        1
    )  # ==> this should simplify to (1, a.x, 1)

    raises(TypeError, lambda: CoordSys3D('a', transformation={
        x: x*sin(y)*cos(z), y:x*sin(y)*sin(z), z:  x*cos(y)}))

