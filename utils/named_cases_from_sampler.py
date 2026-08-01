
def named_cases_from_sampler(gen):
  seen = set()
  retries = 0
  rng = npr.RandomState(42)
  def choose_one(x):
    if not isinstance(x, (list, tuple)):
      x = list(x)
    return [x[rng.randint(len(x))]]
  while (len(seen) < NUM_GENERATED_CASES.value and
         retries < _MAX_CASES_SAMPLING_RETRIES.value):
    retries += 1
    cases = list(gen(choose_one))
    if not cases:
      continue
    if len(cases) > 1:
      raise RuntimeError("Generator is expected to only return a single case when sampling")
    case = cases[0]
    if case["testcase_name"] in seen:
      continue
    retries = 0
    seen.add(case["testcase_name"])
    yield case

