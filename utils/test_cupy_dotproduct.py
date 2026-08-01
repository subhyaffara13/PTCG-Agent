
def test_cupy_dotproduct():
    if not cupy:
        skip("CuPy not installed")

    A = Matrix([x, y, z])
    f1 = lambdify([x, y, z], DotProduct(A, A), modules='cupy')
    f2 = lambdify([x, y, z], DotProduct(A, A.T), modules='cupy')
    f3 = lambdify([x, y, z], DotProduct(A.T, A), modules='cupy')
    f4 = lambdify([x, y, z], DotProduct(A, A.T), modules='cupy')

    assert f1(1, 2, 3) == \
        f2(1, 2, 3) == \
        f3(1, 2, 3) == \
        f4(1, 2, 3) == \
        cupy.array([14])

