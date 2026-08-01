
def test_name():
  assert ds._namespace(add) == ds.getname(add, fqn=True).split('.')
  assert ds._namespace(ts.add) == ds.getname(ts.add, fqn=True).split('.')
  assert ds._namespace(squared) == ds.getname(squared, fqn=True).split('.')
  assert ds._namespace(ts.squared) == ds.getname(ts.squared, fqn=True).split('.')
  assert ds._namespace(Bar) == ds.getname(Bar, fqn=True).split('.')
  assert ds._namespace(ts.Bar) == ds.getname(ts.Bar, fqn=True).split('.')
  assert ds._namespace(tm.quad) == ds.getname(tm.quad, fqn=True).split('.')
  #XXX: the following also works, however behavior may be wrong for nested functions
  #assert ds._namespace(tm.double_add) == ds.getname(tm.double_add, fqn=True).split('.')
  #assert ds._namespace(tm.quadratic) == ds.getname(tm.quadratic, fqn=True).split('.')
  assert ds.getname(add) == 'add'
  assert ds.getname(ts.add) == 'add'
  assert ds.getname(squared) == 'squared'
  assert ds.getname(ts.squared) == 'squared'
  assert ds.getname(Bar) == 'Bar'
  assert ds.getname(ts.Bar) == 'Bar'
  assert ds.getname(tm.quad) == 'quad'
  assert ds.getname(tm.double_add) == 'func' #XXX: ?
  assert ds.getname(tm.quadratic) == 'dec' #XXX: ?

