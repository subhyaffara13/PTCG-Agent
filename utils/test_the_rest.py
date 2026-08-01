
def test_the_rest():
  for obj in [Bar, Foo, Foo.bar, _foo.bar]:
    pyfile = dumpIO_source(obj, alias='_obj')
    _obj = loadIO_source(pyfile)
    assert _obj.__name__ == obj.__name__

