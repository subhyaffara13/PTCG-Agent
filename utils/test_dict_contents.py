
def test_dict_contents():
  c = type.__dict__
  for i,j in c.items():
   #try:
    ok = dill.pickles(j)
   #except Exception:
   #  print ("FAIL: %s with %s" % (i, dill.detect.errors(j)))
    if verbose: print ("%s: %s, %s" % (ok, type(j), j))
    assert ok
  if verbose: print ("")

