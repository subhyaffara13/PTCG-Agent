
def test_MarginalDistribution():
    a1, p1, p2 = symbols('a1 p1 p2', positive=True)
    C = Multinomial('C', 2, p1, p2)
    B = MultivariateBeta('B', a1, C[0])
    MGR = MarginalDistribution(B, (C[0],))
    mgrc = Mul(Symbol('B'), Piecewise(ExprCondPair(Mul(Integer(2),
    Pow(Symbol('p1', positive=True), Indexed(IndexedBase(Symbol('C')),
    Integer(0))), Pow(Symbol('p2', positive=True),
    Indexed(IndexedBase(Symbol('C')), Integer(1))),
    Pow(factorial(Indexed(IndexedBase(Symbol('C')), Integer(0))), Integer(-1)),
    Pow(factorial(Indexed(IndexedBase(Symbol('C')), Integer(1))), Integer(-1))),
    Eq(Add(Indexed(IndexedBase(Symbol('C')), Integer(0)),
    Indexed(IndexedBase(Symbol('C')), Integer(1))), Integer(2))),
    ExprCondPair(Integer(0), True)), Pow(gamma(Symbol('a1', positive=True)),
    Integer(-1)), gamma(Add(Symbol('a1', positive=True),
    Indexed(IndexedBase(Symbol('C')), Integer(0)))),
    Pow(gamma(Indexed(IndexedBase(Symbol('C')), Integer(0))), Integer(-1)),
    Pow(Indexed(IndexedBase(Symbol('B')), Integer(0)),
    Add(Symbol('a1', positive=True), Integer(-1))),
    Pow(Indexed(IndexedBase(Symbol('B')), Integer(1)),
    Add(Indexed(IndexedBase(Symbol('C')), Integer(0)), Integer(-1))))
    assert MGR(C) == mgrc

