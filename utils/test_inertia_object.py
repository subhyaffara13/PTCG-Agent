
def test_inertia_object():
    N = ReferenceFrame('N')
    O = Point('O')
    ixx, iyy, izz = symbols('ixx iyy izz')
    I_dyadic = ixx * (N.x | N.x) + iyy * (N.y | N.y) + izz * (N.z | N.z)
    I = Inertia(inertia(N, ixx, iyy, izz), O)
    assert isinstance(I, tuple)
    assert I.__repr__() == ('Inertia(dyadic=ixx*(N.x|N.x) + iyy*(N.y|N.y) + '
                            'izz*(N.z|N.z), point=O)')
    assert I.dyadic == I_dyadic
    assert I.point == O
    assert I[0] == I_dyadic
    assert I[1] == O
    assert I == (I_dyadic, O)  # Test tuple equal
    raises(TypeError, lambda: I != (O, I_dyadic))  # Incorrect tuple order
    assert I == Inertia(O, I_dyadic)  # Parse changed argument order
    assert I == Inertia.from_inertia_scalars(O, N, ixx, iyy, izz)
    # Test invalid tuple operations
    raises(TypeError, lambda: I + (1, 2))
    raises(TypeError, lambda: (1, 2) + I)
    raises(TypeError, lambda: I * 2)
    raises(TypeError, lambda: 2 * I)

