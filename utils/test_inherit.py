
def test_inherit(): #NOTE: see issue #612
    class Foo:
        w = 0
        x = 1
        y = 1.1
        a = ()
        b = (1,)
        n = None

    class Bar(Foo):
        w = 2
        x = 1
        y = 1.1
        z = 0.2
        a = ()
        b = (1,)
        c = (2,)
        n = None

    Baz = dill.copy(Bar)

    import platform
    is_pypy = platform.python_implementation() == 'PyPy'
    assert Bar.__dict__ == Baz.__dict__
    # ints
    assert 'w' in Bar.__dict__ and 'w' in Baz.__dict__
    assert Bar.__dict__['w'] is Baz.__dict__['w']
    assert 'x' in Bar.__dict__ and 'x' in Baz.__dict__
    assert Bar.__dict__['x'] is Baz.__dict__['x']
    # floats
    assert 'y' in Bar.__dict__ and 'y' in Baz.__dict__
    same = Bar.__dict__['y'] is Baz.__dict__['y']
    assert same if is_pypy else not same
    assert 'z' in Bar.__dict__ and 'z' in Baz.__dict__
    same = Bar.__dict__['z'] is Baz.__dict__['z']
    assert same if is_pypy else not same
    # tuples
    assert 'a' in Bar.__dict__ and 'a' in Baz.__dict__
    assert Bar.__dict__['a'] is Baz.__dict__['a']
    assert 'b' in Bar.__dict__ and 'b' in Baz.__dict__
    assert Bar.__dict__['b'] is not Baz.__dict__['b']
    assert 'c' in Bar.__dict__ and 'c' in Baz.__dict__
    assert Bar.__dict__['c'] is not Baz.__dict__['c']
    # None
    assert 'n' in Bar.__dict__ and 'n' in Baz.__dict__
    assert Bar.__dict__['n'] is Baz.__dict__['n']

