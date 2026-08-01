
def test_issue_18272():
    x = Symbol('x')
    n = Symbol('n')

    assert upretty(ConditionSet(x, Eq(-x + exp(x), 0), S.Complexes)) == \
    '⎧  │         ⎛      x    ⎞⎫\n'\
    '⎨x │ x ∊ ℂ ∧ ⎝-x + ℯ  = 0⎠⎬\n'\
    '⎩  │                      ⎭'
    assert upretty(ConditionSet(x, Contains(n/2, Interval(0, oo)), FiniteSet(-n/2, n/2))) == \
    '⎧  │     ⎧-n   n⎫   ⎛n         ⎞⎫\n'\
    '⎨x │ x ∊ ⎨───, ─⎬ ∧ ⎜─ ∈ [0, ∞)⎟⎬\n'\
    '⎩  │     ⎩ 2   2⎭   ⎝2         ⎠⎭'
    assert upretty(ConditionSet(x, Eq(Piecewise((1, x >= 3), (x/2 - 1/2, x >= 2), (1/2, x >= 1),
                (x/2, True)) - 1/2, 0), Interval(0, 3))) == \
    '⎧  │              ⎛⎛⎧   1     for x ≥ 3⎞          ⎞⎫\n'\
    '⎪  │              ⎜⎜⎪                  ⎟          ⎟⎪\n'\
    '⎪  │              ⎜⎜⎪x                 ⎟          ⎟⎪\n'\
    '⎪  │              ⎜⎜⎪─ - 0.5  for x ≥ 2⎟          ⎟⎪\n'\
    '⎪  │              ⎜⎜⎪2                 ⎟          ⎟⎪\n'\
    '⎨x │ x ∊ [0, 3] ∧ ⎜⎜⎨                  ⎟ - 0.5 = 0⎟⎬\n'\
    '⎪  │              ⎜⎜⎪  0.5    for x ≥ 1⎟          ⎟⎪\n'\
    '⎪  │              ⎜⎜⎪                  ⎟          ⎟⎪\n'\
    '⎪  │              ⎜⎜⎪   x              ⎟          ⎟⎪\n'\
    '⎪  │              ⎜⎜⎪   ─     otherwise⎟          ⎟⎪\n'\
    '⎩  │              ⎝⎝⎩   2              ⎠          ⎠⎭'

