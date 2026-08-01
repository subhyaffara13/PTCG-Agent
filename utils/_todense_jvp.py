
def _todense_jvp(primals, tangents, *, tree):
  assert not isinstance(tangents[0], ad.Zero)
  assert all(isinstance(t, ad.Zero) for t in tangents[1:])
  primals_out = todense_p.bind(*primals, tree=tree)
  tangents_out = todense_p.bind(tangents[0], *primals[1:], tree=tree)
  return primals_out, tangents_out

