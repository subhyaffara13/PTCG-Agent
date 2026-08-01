
def test_isfrommain():
  assert ds.isfrommain(add) == True
  assert ds.isfrommain(squared) == True
  assert ds.isfrommain(Bar) == True
  assert ds.isfrommain(_bar) == True
  assert ds.isfrommain(ts.add) == False
  assert ds.isfrommain(ts.squared) == False
  assert ds.isfrommain(ts.Bar) == False
  assert ds.isfrommain(ts._bar) == False
  assert ds.isfrommain(tm.quad) == False
  assert ds.isfrommain(tm.double_add) == False
  assert ds.isfrommain(tm.quadratic) == False
  assert ds.isdynamic(add) == False
  assert ds.isdynamic(squared) == False
  assert ds.isdynamic(ts.add) == False
  assert ds.isdynamic(ts.squared) == False
  assert ds.isdynamic(tm.double_add) == False
  assert ds.isdynamic(tm.quadratic) == False

