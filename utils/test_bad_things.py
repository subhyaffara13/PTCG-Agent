
def test_bad_things():
    f = inspect.currentframe()
    assert baditems(f) == [f]
    #assert baditems(globals()) == [f] #XXX
    assert badobjects(f) is f
    assert badtypes(f) == type(f)
    assert type(errors(f)) is TypeError
    d = badtypes(f, 1)
    assert isinstance(d, dict)
    assert list(badobjects(f, 1).keys()) == list(d.keys())
    assert list(errors(f, 1).keys()) == list(d.keys())
    s = set([(err.__class__.__name__,err.args[0]) for err in list(errors(f, 1).values())])
    a = dict(s)
    if not os.environ.get('COVERAGE'): #XXX: travis-ci
        proxy = 0 if type(f.f_locals) is dict else 1
        assert len(s) == len(a) + proxy # TypeError (and possibly PicklingError)
    n = 2
    assert len(a) is n if 'PicklingError' in a.keys() else n-1

