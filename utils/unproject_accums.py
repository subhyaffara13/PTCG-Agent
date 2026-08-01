
def unproject_accums(specs, result):
  args, result_ = [], iter(result)
  for k, aval in specs:
    if k is ValAccum:
      args.append(ValAccum(aval))
    elif k is RefAccum:
      args.append(RefAccum(aval, next(result_)))
    elif k is NullAccum:
      args.append(NullAccum(aval))
    elif k is None:
      args.append(next(result_))
    else:
      assert False
  assert next(result_, None) is None
  return args

