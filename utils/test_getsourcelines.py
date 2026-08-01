
def test_getsourcelines():
  assert ''.join(ds.getsourcelines(add)[0]) == 'def add(x,y):\n  return x+y\n'
  assert ''.join(ds.getsourcelines(ts.add)[0]) == 'def add(x,y):\n  return x+y\n'
  assert ''.join(ds.getsourcelines(squared)[0]) == 'squared = lambda x:x**2\n'
  assert ''.join(ds.getsourcelines(ts.squared)[0]) == 'squared = lambda x:x**2\n'
  assert ''.join(ds.getsourcelines(Bar)[0]) == 'class Bar:\n  pass\n'
  assert ''.join(ds.getsourcelines(ts.Bar)[0]) == 'class Bar:\n  pass\n'
  assert ''.join(ds.getsourcelines(_bar)[0]) == 'class Bar:\n  pass\n' #XXX: ?
  assert ''.join(ds.getsourcelines(ts._bar)[0]) == 'class Bar:\n  pass\n' #XXX: ?
  assert ''.join(ds.getsourcelines(tm.quad)[0]) == 'def quad(a=1, b=1, c=0):\n  inverted = [False]\n  def invert():\n    inverted[0] = not inverted[0]\n  def dec(f):\n    def func(*args, **kwds):\n      x = f(*args, **kwds)\n      if inverted[0]: x = -x\n      return a*x**2 + b*x + c\n    func.__wrapped__ = f\n    func.invert = invert\n    func.inverted = inverted\n    return func\n  return dec\n'
  assert ''.join(ds.getsourcelines(tm.quadratic)[0]) == '  def dec(f):\n    def func(*args,**kwds):\n      fx = f(*args,**kwds)\n      return a*fx**2 + b*fx + c\n    return func\n'
  assert ''.join(ds.getsourcelines(tm.quadratic, lstrip=True)[0]) == 'def dec(f):\n  def func(*args,**kwds):\n    fx = f(*args,**kwds)\n    return a*fx**2 + b*fx + c\n  return func\n'
  assert ''.join(ds.getsourcelines(tm.quadratic, enclosing=True)[0]) == 'def quad_factory(a=1,b=1,c=0):\n  def dec(f):\n    def func(*args,**kwds):\n      fx = f(*args,**kwds)\n      return a*fx**2 + b*fx + c\n    return func\n  return dec\n'
  assert ''.join(ds.getsourcelines(tm.double_add)[0]) == '    def func(*args, **kwds):\n      x = f(*args, **kwds)\n      if inverted[0]: x = -x\n      return a*x**2 + b*x + c\n'
  assert ''.join(ds.getsourcelines(tm.double_add, enclosing=True)[0]) == 'def quad(a=1, b=1, c=0):\n  inverted = [False]\n  def invert():\n    inverted[0] = not inverted[0]\n  def dec(f):\n    def func(*args, **kwds):\n      x = f(*args, **kwds)\n      if inverted[0]: x = -x\n      return a*x**2 + b*x + c\n    func.__wrapped__ = f\n    func.invert = invert\n    func.inverted = inverted\n    return func\n  return dec\n'

