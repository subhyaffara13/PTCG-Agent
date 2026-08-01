
def test_safe():
  import abc
  obj = abc.ABC()
  obj.__class__.__name__ = "(abc' + print('foo')]) # "
  try:
    source = getsource(obj, force=True)
    assert False
  except TypeError:
    assert False
  except SyntaxError:
    pass

