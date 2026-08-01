
def test_importable():
  assert importable(add, source=False) == 'from %s import add\n' % __name__
  assert importable(squared, source=False) == 'from %s import squared\n' % __name__
  assert importable(Foo, source=False) == 'from %s import Foo\n' % __name__
  assert importable(Foo.bar, source=False) == 'from %s import bar\n' % __name__
  assert importable(_foo.bar, source=False) == 'from %s import bar\n' % __name__
  assert importable(None, source=False) == 'None\n'
  assert importable(100, source=False) == '100\n'

  assert importable(add, source=True) == 'def add(x,y):\n  return x+y\n'
  assert importable(squared, source=True) == 'squared = lambda x:x**2\n'
  assert importable(None, source=True) == 'None\n'
  assert importable(Bar, source=True) == 'class Bar:\n  pass\n'
  assert importable(Foo, source=True) == 'class Foo(object):\n  def bar(self, x):\n    return x*x+x\n'
  assert importable(Foo.bar, source=True) == 'def bar(self, x):\n  return x*x+x\n'
  assert importable(Foo.bar, source=False) == 'from %s import bar\n' % __name__
  assert importable(Foo.bar, alias='memo', source=False) == 'from %s import bar as memo\n' % __name__
  assert importable(Foo, alias='memo', source=False) == 'from %s import Foo as memo\n' % __name__
  assert importable(squared, alias='memo', source=False) == 'from %s import squared as memo\n' % __name__
  assert importable(squared, alias='memo', source=True) == 'memo = squared = lambda x:x**2\n'
  assert importable(add, alias='memo', source=True) == 'def add(x,y):\n  return x+y\n\nmemo = add\n'
  assert importable(None, alias='memo', source=True) == 'memo = None\n'
  assert importable(100, alias='memo', source=True) == 'memo = 100\n'
  assert importable(add, builtin=True, source=False) == 'from %s import add\n' % __name__
  assert importable(squared, builtin=True, source=False) == 'from %s import squared\n' % __name__
  assert importable(Foo, builtin=True, source=False) == 'from %s import Foo\n' % __name__
  assert importable(Foo.bar, builtin=True, source=False) == 'from %s import bar\n' % __name__
  assert importable(_foo.bar, builtin=True, source=False) == 'from %s import bar\n' % __name__
  assert importable(None, builtin=True, source=False) == 'None\n'
  assert importable(100, builtin=True, source=False) == '100\n'


def test_importable():
  assert ds.importable(add, source=False) == ds.getimport(add)
  assert ds.importable(add) == ds.getsource(add)
  assert ds.importable(squared, source=False) == ds.getimport(squared)
  assert ds.importable(squared) == ds.getsource(squared)
  assert ds.importable(Bar, source=False) == ds.getimport(Bar)
  assert ds.importable(Bar) == ds.getsource(Bar)
  assert ds.importable(ts.add) == ds.getimport(ts.add)
  assert ds.importable(ts.add, source=True) == ds.getsource(ts.add)
  assert ds.importable(ts.squared) == ds.getimport(ts.squared)
  assert ds.importable(ts.squared, source=True) == ds.getsource(ts.squared)
  assert ds.importable(ts.Bar) == ds.getimport(ts.Bar)
  assert ds.importable(ts.Bar, source=True) == ds.getsource(ts.Bar)

