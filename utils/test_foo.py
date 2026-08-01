
def test_foo():
  assert importable(_foo, source=True).startswith("import dill\nclass Foo(object):\n  def bar(self, x):\n    return x*x+x\ndill.loads(")

