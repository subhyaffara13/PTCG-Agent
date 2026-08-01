
def test_two_arg_functions():
  for obj in [add]:
    pyfile = dumpIO_source(obj, alias='_obj')
    _obj = loadIO_source(pyfile)
    assert _obj(4,2) == obj(4,2)

