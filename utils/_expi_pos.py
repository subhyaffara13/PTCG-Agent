
def _expi_pos(x: Array) -> Array:
  # x >= 0
  _c = _lax_const
  conds = [(_c(x, 0) < x) & (x <= _c(x, 2))] + [
    (_c(x, 2 ** i) < x) & (x <= _c(x, 2 ** (i + 1))) for i in range(1, 6)
  ]
  return jnp.piecewise(
    x,
    conds,
    [_expint1, _expint2, _expint3, _expint4, _expint5, _expint6, _expint7],
  )

