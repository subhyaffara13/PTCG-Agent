
def test_add3():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    i0, i1 = tensor_indices('i0:2', Lorentz)
    E, px, py, pz = symbols('E px py pz')
    A = TensorHead('A', [Lorentz])
    B = TensorHead('B', [Lorentz])

    expr1 = A(i0)*A(-i0) - (E**2 - px**2 - py**2 - pz**2)
    assert expr1.args == (-E**2, px**2, py**2, pz**2, A(i0)*A(-i0))

    expr2 = E**2 - px**2 - py**2 - pz**2 - A(i0)*A(-i0)
    assert expr2.args == (E**2, -px**2, -py**2, -pz**2, -A(i0)*A(-i0))

    expr3 = A(i0)*A(-i0) - E**2 + px**2 + py**2 + pz**2
    assert expr3.args == (-E**2, px**2, py**2, pz**2, A(i0)*A(-i0))

    expr4 = B(i1)*B(-i1) + 2*E**2 - 2*px**2 - 2*py**2 - 2*pz**2 - A(i0)*A(-i0)
    assert expr4.args == (2*E**2, -2*px**2, -2*py**2, -2*pz**2, B(i1)*B(-i1), -A(i0)*A(-i0))

