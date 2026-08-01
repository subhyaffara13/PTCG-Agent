
def _empty_array(prefix, length_spec, aval):
  sharding = aval.sharding.update(spec=aval.sharding.spec.update(
      partitions=(*length_spec, *aval.sharding.spec.partitions)))
  # TODO(yashkatariya): Replace `lax.empty2` with `lax.empty` once
  # AllocateBuffer issues are fixed. Also delete `empty2` after this usage is
  # removed. Basically uncomment the following 2 lines.
  # lax.empty will also need to take a memory_space argument.
  # empty = lax.empty((*prefix, *aval.shape), aval.dtype, out_sharding=sharding,
  #                   memory_space=aval.memory_space)
  # return core.pvary(empty, tuple(aval.mat.varying))
  empty = core.pvary(lax.empty2(aval.dtype, memory_space=aval.memory_space),
                     tuple(aval.mat.varying))
  with use_abstract_mesh(sharding.mesh):
    out = lax.broadcast(empty, (*prefix, *aval.shape), out_sharding=sharding)
  return out

