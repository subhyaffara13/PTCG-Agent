
def test_issue_12657():
    # treat -oo like the atom that it is
    reps = [(-oo, 1), (oo, 2)]
    assert (x < -oo).subs(reps) == (x < 1)
    assert (x < -oo).subs(list(reversed(reps))) == (x < 1)
    reps = [(-oo, 2), (oo, 1)]
    assert (x < oo).subs(reps) == (x < 1)
    assert (x < oo).subs(list(reversed(reps))) == (x < 1)

