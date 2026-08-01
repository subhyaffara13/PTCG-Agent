
def _shard_ref(mesh, auto, check_rep, names, ref_aval: AbstractRef):
  aval = core.shard_aval(mesh, auto, check_rep, names, ref_aval.inner_aval)
  return AbstractRef(aval)

