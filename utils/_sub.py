
def _sub(c1, c2):
    """ Helper function used to implement the ``<type>sub`` functions. """
    # c1, c2 are trimmed copies
    [c1, c2] = as_series([c1, c2])
    if len(c1) > len(c2):
        c1[:c2.size] -= c2
        ret = c1
    else:
        c2 = -c2
        c2[:c1.size] += c1
        ret = c2
    return trimseq(ret)


def _sub(x: ir.Value, y: ir.Value) -> ir.Value:
  x_element_type = _element_type(x.type)
  y_element_type = _element_type(y.type)
  if _is_triton_pointer_type(x_element_type):
    return tt_dialect.addptr(x.type, x, _minus(y))
  elif not _is_triton_pointer_type(y_element_type):
    assert x.type == y.type, (str(x.type), str(y.type))
    if isinstance(x_element_type, ir.IntegerType):
      return arith_dialect.subi(x, y)
    elif isinstance(x_element_type, ir.FloatType):
      return arith_dialect.subf(x, y)
  raise NotImplementedError(f"unsupported dtype: {y.type}")

