
def broadcast_batcher(prim, axis_data, args, dims, **params):
  assert len(args) > 1
  if all(d is None for d in dims):
    o = prim.bind(*args, **params)
    return (o, [None] * len(o)) if prim.multiple_results else (o, None)
  shape, dim = next((x.shape, d) for x, d in zip(args, dims)
                    if d is not None)
  if all(core.definitely_equal_shape(shape, x.shape) and d == dim
         for x, d in zip(args, dims) if np.ndim(x)):
    # if there's only agreeing batch dims and scalars, just call the primitive
    args = spmd_names_insert_pvary(*args)
    out = prim.bind(*args, **params)
    return (out, (dim,) * len(out)) if prim.multiple_results else (out, dim)
  else:
    # We pass size of 1 here because (1) at least one argument has a real batch
    # dimension and (2) all unmapped axes can have a singleton axis inserted and
    # then rely on the primitive's built-in broadcasting.
    args = [bdim_at_front(x, d, 1) if np.ndim(x) else x
            for x, d in zip(args, dims)]
    ndim = max(np.ndim(x) for x in args)  # special-case scalar broadcasting
    args = [_handle_scalar_broadcasting(ndim, x, d) for x, d in zip(args, dims)]
    out = prim.bind(*args, **params)
    return (out, (0,) * len(out)) if prim.multiple_results else (out, 0)

