
def test_summation_by_residues_failing():
    x = Symbol('x')

    # Failing because of the bug in residue computation
    assert eval_sum_residue(x**2 / (x**4 + 1), (x, S(1), oo))
    assert eval_sum_residue(1 / ((x - 1)*(x - 2) + 1), (x, -oo, oo)) != 0

