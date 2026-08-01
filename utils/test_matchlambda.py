
def test_matchlambda():
  assert ds._matchlambda(f, 'f = lambda x: x**2\n')
  assert ds._matchlambda(squared, 'squared = lambda x:x**2\n')
  assert ds._matchlambda(ts.f, 'f = lambda x: x**2\n')
  assert ds._matchlambda(ts.squared, 'squared = lambda x:x**2\n')

