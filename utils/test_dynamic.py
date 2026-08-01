
def test_dynamic():
  assert getimport(add) == 'from %s import add\n' % __name__
  # interactive lambdas
  assert getimport(squared) == 'from %s import squared\n' % __name__

