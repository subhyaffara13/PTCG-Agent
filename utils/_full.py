from typing import Any

def _full(fill_value, device, dtype, size):
    value = fill_value
    if not isinstance(fill_value, (int, float)) and hasattr(value, "value"):
        value = value.value

    if isinstance(value, (int, float)):

        def inner_fn(index):
            return ops.constant(value, dtype)

    elif isinstance(value, sympy.Basic):

        def inner_fn(index):
            return ops.index_expr(value, dtype)

    else:
        assert len(value.get_size()) == 0
        value_loader = value.make_loader()

        def inner_fn(index):
            return value_loader([])

    return Pointwise.create(
        device=device,
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=list(size),
    )


def _full(t: ir.Type, v: Any) -> ir.Value:
  element_type = _element_type(t)
  if isinstance(element_type, ir.IntegerType):
    result = arith_dialect.constant(element_type, int(v))
  elif isinstance(element_type, ir.FloatType):
    result = arith_dialect.constant(element_type, float(v))
  else:
    raise NotImplementedError

  if isinstance(t, ir.RankedTensorType):
    return tt_dialect.splat(t, result)
  else:
    return result

