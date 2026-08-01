
def test_class():
    msg = (
        rf"Starting with pandas version {WARNING_CATEGORY.version()} all arguments "
        r"of Foo\.baz except for the argument \'bar\' will be keyword-only"
    )
    with tm.assert_produces_warning(WARNING_CATEGORY, match=msg):
        Foo().baz("qux", "quox")


def test_class():
  o = _d()
  oo = _newclass()
  ok = dill.pickles(o)
  if verbose: print ("%s: %s, %s" % (ok, type(o), o))
  assert ok
  ok = dill.pickles(oo)
  if verbose: print ("%s: %s, %s" % (ok, type(oo), oo))
  assert ok
  if verbose: print ("")

