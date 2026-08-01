
def _make_lengths_same(sharding, ndim):
  pspec = sharding.spec
  if ndim > len(pspec):
    return sharding.update(spec=pspec._normalized_spec_for_aval(ndim))
  if ndim < len(pspec):
    assert all(s is None for s in pspec[ndim:]), (ndim, pspec)
    return sharding.update(spec=P(*pspec[:ndim], unreduced=pspec.unreduced,
                                  reduced=pspec.reduced))
  assert False, "unreachable"

