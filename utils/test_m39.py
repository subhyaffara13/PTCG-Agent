
def test_M39():
    x, y, z = symbols('x y z', complex=True)
    # TODO: Replace solve with solveset, as of now
    # solveset doesn't supports non-linear multivariate
    assert solve([x**2*y + 3*y*z - 4, -3*x**2*z + 2*y**2 + 1, 2*y*z**2 - z**2 - 1 ]) ==\
            [{y: 1, z: 1, x: -1}, {y: 1, z: 1, x: 1},\
             {y: sqrt(2)*I, z: R(1,3) - sqrt(2)*I/3, x: -sqrt(-1 - sqrt(2)*I)},\
             {y: sqrt(2)*I, z: R(1,3) - sqrt(2)*I/3, x: sqrt(-1 - sqrt(2)*I)},\
             {y: -sqrt(2)*I, z: R(1,3) + sqrt(2)*I/3, x: -sqrt(-1 + sqrt(2)*I)},\
             {y: -sqrt(2)*I, z: R(1,3) + sqrt(2)*I/3, x: sqrt(-1 + sqrt(2)*I)}]

