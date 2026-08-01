
def empty_like_shaped_array(aval):
  out = core.pvary(empty2(aval.dtype, memory_space=aval.memory_space),
                   tuple(aval.mat.varying))
  with use_abstract_mesh(aval.sharding.mesh):
    return broadcast(out, aval.shape, out_sharding=aval.sharding)

