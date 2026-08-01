
def test_builtin():
  assert getimport(pow) == 'pow\n'
  assert getimport(100) == '100\n'
  assert getimport(True) == 'True\n'
  assert getimport(pow, builtin=True) == 'from builtins import pow\n'
  assert getimport(100, builtin=True) == '100\n'
  assert getimport(True, builtin=True) == 'True\n'
  # this is kinda BS... you can't import a None
  assert getimport(None) == 'None\n'
  assert getimport(None, builtin=True) == 'None\n'

