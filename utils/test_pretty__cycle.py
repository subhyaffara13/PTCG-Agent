
def test_pretty_Cycle():
    from sympy.combinatorics.permutations import Cycle
    assert pretty(Cycle(1, 2)) == '(1 2)'
    assert pretty(Cycle(2)) == '(2)'
    assert pretty(Cycle(1, 3)(4, 5)) == '(1 3)(4 5)'
    assert pretty(Cycle()) == '()'

