
def test_inconsistent():
    # cf. issues 5795 and 5545
    raises(InconsistentAssumptions, lambda: Symbol('x', real=True,
           commutative=False))

