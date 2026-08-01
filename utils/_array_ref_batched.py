
def _array_ref_batched(axis_data, vals_in, dims_in, memory_space, kind):
  val, = vals_in
  dim, = dims_in
  if dim is None:
    # We defensively batch the ref, b/c it could later be hit with a batched val
    val2 = batching.broadcast(val, axis_data.size, 0,
                              axis_data.explicit_mesh_axis)
    return core.ref_p.bind(val2, memory_space=memory_space, kind=kind), 0
  else:
    return core.ref_p.bind(val, memory_space=memory_space, kind=kind), dim

