
def addupdate_transpose_fancy(cts_in, ref_, x, *idx, **params):
  if ref_.ref is not None and isinstance(x, ad.GradAccum):
    x_bar = get_p.bind(ref_.ref, *idx, **params)
    x.accum(x_bar)

