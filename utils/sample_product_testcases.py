
def sample_product_testcases(*args, **kw):
  """Non-decorator form of sample_product."""
  args = [list(arg) for arg in args]
  kw = [(k, list(v)) for k, v in kw.items()]
  n = math.prod(len(a) for a in args) * math.prod(len(v) for _, v in kw)
  testcases = []
  for i in _choice(n, min(n, NUM_GENERATED_CASES.value)):
    testcase = {}
    for a in args:
      testcase.update(a[i % len(a)])
      i //= len(a)
    for k, v in kw:
      testcase[k] = v[i % len(v)]
      i //= len(v)
    testcases.append(testcase)
  return testcases

