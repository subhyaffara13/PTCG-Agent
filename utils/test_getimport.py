
def test_getimport():
  local = {}
  exec(ds.getimport(add, alias='raw'), {}, local)
  exec(ds.getimport(ts.add, alias='mod'), {}, local)
  assert local['raw'](1,2) == local['mod'](1,2)
  exec(ds.getimport(squared, alias='raw'), {}, local)
  exec(ds.getimport(ts.squared, alias='mod'), {}, local)
  assert local['raw'](3) == local['mod'](3)
  exec(ds.getimport(Bar, alias='raw'), {}, local)
  exec(ds.getimport(ts.Bar, alias='mod'), {}, local)
  assert ds.getname(local['raw']) == ds.getname(local['mod'])
  exec(ds.getimport(tm.quad, alias='mod'), {}, local)
  assert local['mod']()(sum)([1,2,3]) == tm.quad()(sum)([1,2,3])

