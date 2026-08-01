
def test_Tr():
    #TODO: Handle indices
    A, B = symbols('A B', commutative=False)
    t = Tr(A*B)
    assert latex(t) == r'\operatorname{tr}\left(A B\right)'


def test_Tr():
    A, B = symbols('A B', commutative=False)
    t = Tr(A*B)
    assert str(t) == 'Tr(A*B)'


def test_Tr():
    A, B = symbols('A B', commutative=False)
    t = Tr(A*B)
    assert pretty(t) == r'Tr(A*B)'
    assert upretty(t) == 'Tr(A⋅B)'

