
def test_deprecated_moved_functions():
    from sympy.physics.mechanics.functions import (
        inertia, inertia_of_point_mass, gravity)
    N = ReferenceFrame('N')
    with warns_deprecated_sympy():
        assert inertia(N, 0, 1, 0, 1) == (N.x | N.y) + (N.y | N.x) + (N.y | N.y)
    with warns_deprecated_sympy():
        assert inertia_of_point_mass(1, N.x + N.y, N) == (
            (N.x | N.x) + (N.y | N.y) + 2 * (N.z | N.z) -
            (N.x | N.y) - (N.y | N.x))
    p = Particle('P')
    with warns_deprecated_sympy():
        assert gravity(-2 * N.z, p) == [(p.masscenter, -2 * p.mass * N.z)]

