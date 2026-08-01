
def test_represent():
    x, y = symbols('x y')
    d = Density([XKet(), 0.5], [PxKet(), 0.5])
    assert (represent(0.5*(PxKet()*Dagger(PxKet()))) +
            represent(0.5*(XKet()*Dagger(XKet())))) == represent(d)

    # check for kets with expr in them
    d_with_sym = Density([XKet(x*y), 0.5], [PxKet(x*y), 0.5])
    assert (represent(0.5*(PxKet(x*y)*Dagger(PxKet(x*y)))) +
            represent(0.5*(XKet(x*y)*Dagger(XKet(x*y))))) == \
        represent(d_with_sym)

    # check when given explicit basis
    assert (represent(0.5*(XKet()*Dagger(XKet())), basis=PxOp()) +
            represent(0.5*(PxKet()*Dagger(PxKet())), basis=PxOp())) == \
        represent(d, basis=PxOp())


def test_represent():
    assert represent(sx) == Matrix([[0, 1], [1, 0]])
    assert represent(sy) == Matrix([[0, -I], [I, 0]])
    assert represent(sz) == Matrix([[1, 0], [0, -1]])
    assert represent(sm) == Matrix([[0, 0], [1, 0]])
    assert represent(sp) == Matrix([[0, 1], [0, 0]])

