
def empty_ref(ty, memory_space=None):
  aval = shaped_abstractify(ty)
  return empty_ref_p.bind(ty=aval, memory_space=memory_space)

