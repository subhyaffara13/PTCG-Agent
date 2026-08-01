
def _swap_transpose_fancy(g, ref_, x, *idx, **params):
  if ref_.ref is None and type(g) is ad_util.Zero:
    return
  elif ref_.ref is None:
    swap_p.bind(ref_.inst().ref, ad_util.instantiate(g), *idx, **params)
  else:
    x_bar = swap_p.bind(ref_.inst().ref, ad_util.instantiate(g), *idx, **params)
    x.accum(x_bar)

