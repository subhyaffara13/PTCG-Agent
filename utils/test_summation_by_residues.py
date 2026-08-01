
def test_summation_by_residues():
    x = Symbol('x')

    # Examples from Nakhle H. Asmar, Loukas Grafakos,
    # Complex Analysis with Applications
    assert eval_sum_residue(1 / (x**2 + 1), (x, -oo, oo)) == pi/tanh(pi)
    assert eval_sum_residue(1 / x**6, (x, S(1), oo)) == pi**6/945
    assert eval_sum_residue(1 / (x**2 + 9), (x, -oo, oo)) == pi/(3*tanh(3*pi))
    assert eval_sum_residue(1 / (x**2 + 1)**2, (x, -oo, oo)).cancel() == \
        (-pi**2*tanh(pi)**2 + pi*tanh(pi) + pi**2)/(2*tanh(pi)**2)
    assert eval_sum_residue(x**2 / (x**2 + 1)**2, (x, -oo, oo)).cancel() == \
        (-pi**2 + pi*tanh(pi) + pi**2*tanh(pi)**2)/(2*tanh(pi)**2)
    assert eval_sum_residue(1 / (4*x**2 - 1), (x, -oo, oo)) == 0
    assert eval_sum_residue(x**2 / (x**2 - S(1)/4)**2, (x, -oo, oo)) == pi**2/2
    assert eval_sum_residue(1 / (4*x**2 - 1)**2, (x, -oo, oo)) == pi**2/8
    assert eval_sum_residue(1 / ((x - S(1)/2)**2 + 1), (x, -oo, oo)) == pi*tanh(pi)
    assert eval_sum_residue(1 / x**2, (x, S(1), oo)) == pi**2/6
    assert eval_sum_residue(1 / x**4, (x, S(1), oo)) == pi**4/90
    assert eval_sum_residue(1 / x**2 / (x**2 + 4), (x, S(1), oo)) == \
        -pi*(-pi/12 - 1/(16*pi) + 1/(8*tanh(2*pi)))/2

    # Some examples made from 1 / (x**2 + 1)
    assert eval_sum_residue(1 / (x**2 + 1), (x, S(0), oo)) == \
        S(1)/2 + pi/(2*tanh(pi))
    assert eval_sum_residue(1 / (x**2 + 1), (x, S(1), oo)) == \
        -S(1)/2 + pi/(2*tanh(pi))
    assert eval_sum_residue(1 / (x**2 + 1), (x, S(-1), oo)) == \
        1 + pi/(2*tanh(pi))
    assert eval_sum_residue((-1)**x / (x**2 + 1), (x, -oo, oo)) == \
        pi/sinh(pi)
    assert eval_sum_residue((-1)**x / (x**2 + 1), (x, S(0), oo)) == \
        pi/(2*sinh(pi)) + S(1)/2
    assert eval_sum_residue((-1)**x / (x**2 + 1), (x, S(1), oo)) == \
        -S(1)/2 + pi/(2*sinh(pi))
    assert eval_sum_residue((-1)**x / (x**2 + 1), (x, S(-1), oo)) == \
        pi/(2*sinh(pi))

    # Some examples made from shifting of 1 / (x**2 + 1)
    assert eval_sum_residue(1 / (x**2 + 2*x + 2), (x, S(-1), oo)) == S(1)/2 + pi/(2*tanh(pi))
    assert eval_sum_residue(1 / (x**2 + 4*x + 5), (x, S(-2), oo)) == S(1)/2 + pi/(2*tanh(pi))
    assert eval_sum_residue(1 / (x**2 - 2*x + 2), (x, S(1), oo)) == S(1)/2 + pi/(2*tanh(pi))
    assert eval_sum_residue(1 / (x**2 - 4*x + 5), (x, S(2), oo)) == S(1)/2 + pi/(2*tanh(pi))
    assert eval_sum_residue((-1)**x * -1 / (x**2 + 2*x + 2), (x, S(-1), oo)) ==  S(1)/2 + pi/(2*sinh(pi))
    assert eval_sum_residue((-1)**x * -1 / (x**2 -2*x + 2), (x, S(1), oo)) == S(1)/2 + pi/(2*sinh(pi))

    # Some examples made from 1 / x**2
    assert eval_sum_residue(1 / x**2, (x, S(2), oo)) == -1 + pi**2/6
    assert eval_sum_residue(1 / x**2, (x, S(3), oo)) == -S(5)/4 + pi**2/6
    assert eval_sum_residue((-1)**x / x**2, (x, S(1), oo)) == -pi**2/12
    assert eval_sum_residue((-1)**x / x**2, (x, S(2), oo)) == 1 - pi**2/12

