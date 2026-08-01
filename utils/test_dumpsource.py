
def test_dumpsource():
  local = {}
  exec(ds.dumpsource(add, alias='raw'), {}, local)
  exec(ds.dumpsource(ts.add, alias='mod'), {}, local)
  assert local['raw'](1,2) == local['mod'](1,2)
  exec(ds.dumpsource(squared, alias='raw'), {}, local)
  exec(ds.dumpsource(ts.squared, alias='mod'), {}, local)
  assert local['raw'](3) == local['mod'](3)
  assert ds._wrap(add)(1,2) == ds._wrap(ts.add)(1,2)
  assert ds._wrap(squared)(3) == ds._wrap(ts.squared)(3)

