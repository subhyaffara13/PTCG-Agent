
def _make_index(s):
  if isinstance(s, (int, np.ndarray)):
    return ir_constant(s, ir.IndexType.get())
  if s.type == ir.IndexType.get():
    return s
  return arith.index_cast(ir.IndexType.get(), s)

