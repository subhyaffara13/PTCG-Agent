
def _abs_jvp_rule(g, ans, x):
  if _iscomplex(x):
    return _maybe_real(mul(g, div(_maybe_conj(x),
           _replace_zero(convert_element_type(ans, _dtype(x))))))
  else:
    return select(ge(x, _zero(x)), g, neg(g))

