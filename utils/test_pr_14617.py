
def test_PR_14617():
    from sympy.functions.combinatorial.numbers import nT
    for n in (0, []):
        for k in (-1, 0, 1):
            if k == 0:
                assert nT(n, k) == 1
            else:
                assert nT(n, k) == 0

