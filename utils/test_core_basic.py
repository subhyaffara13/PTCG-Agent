
def test_core_basic():
    for c in (Atom, Atom(), Basic, Basic(), SingletonRegistry, S):
        check(c)

