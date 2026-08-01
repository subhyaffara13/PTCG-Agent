
def test_imported():
  from math import sin
  assert getimport(sin) == 'from math import sin\n'

