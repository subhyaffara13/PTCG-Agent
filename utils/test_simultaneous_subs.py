
def test_simultaneous_subs():
    reps = {x: 0, y: 0}
    assert (x/y).subs(reps) != (y/x).subs(reps)
    assert (x/y).subs(reps, simultaneous=True) == \
        (y/x).subs(reps, simultaneous=True)
    reps = reps.items()
    assert (x/y).subs(reps) != (y/x).subs(reps)
    assert (x/y).subs(reps, simultaneous=True) == \
        (y/x).subs(reps, simultaneous=True)
    assert Derivative(x, y, z).subs(reps, simultaneous=True) == \
        Subs(Derivative(0, y, z), y, 0)

