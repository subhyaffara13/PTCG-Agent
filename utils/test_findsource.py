
def test_findsource():
  lines, lineno = ds.findsource(add)
  assert lines[lineno] == 'def add(x,y):\n'
  lines, lineno = ds.findsource(ts.add)
  assert lines[lineno] == 'def add(x,y):\n'
  lines, lineno = ds.findsource(squared)
  assert lines[lineno] == 'squared = lambda x:x**2\n'
  lines, lineno = ds.findsource(ts.squared)
  assert lines[lineno] == 'squared = lambda x:x**2\n'
  lines, lineno = ds.findsource(Bar)
  assert lines[lineno] == 'class Bar:\n'
  lines, lineno = ds.findsource(ts.Bar)
  assert lines[lineno] == 'class Bar:\n'
  lines, lineno = ds.findsource(_bar)
  assert lines[lineno] == 'class Bar:\n'
  lines, lineno = ds.findsource(ts._bar)
  assert lines[lineno] == 'class Bar:\n'
  lines, lineno = ds.findsource(tm.quad)
  assert lines[lineno] == 'def quad(a=1, b=1, c=0):\n'
  lines, lineno = ds.findsource(tm.double_add)
  assert lines[lineno] == '    def func(*args, **kwds):\n'
  lines, lineno = ds.findsource(tm.quadratic)
  assert lines[lineno] == '  def dec(f):\n'

