
def _physicalize_transform(f, *args):
  vals, zeros = args[::2], args[1::2]
  assert len(vals) == len(zeros)
  wrapper = lambda *inner_vals: f(
      *it.chain.from_iterable(zip(inner_vals, zeros))
  )
  return physicalize(wrapper)(*vals)

