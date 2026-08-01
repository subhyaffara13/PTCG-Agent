
def _insert_pvary(basis, leaf):
  if not config._check_vma.value or not config.auto_pcast.value:
    return basis
  return core.pvary(basis, tuple(core.typeof(leaf).mat.varying))

