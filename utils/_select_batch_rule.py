
def _select_batch_rule(axis_data, batched_args, batch_dims, **unused_kwargs):
  which, *cases = batched_args
  which_bdim, *case_bdims = batch_dims
  if all(bdim is None for bdim in batch_dims):
    out = select_n_p.bind(which, *cases, **unused_kwargs)
    return out, None

  size = next(x.shape[i] for x, i in zip(batched_args, batch_dims)
              if i is not None)

  # avoid transposes and some broadcasts in special cases
  if all(which_bdim == bdim for bdim in case_bdims):
    if np.shape(which) == np.shape(cases[0]):
      return select_n(which, *cases), which_bdim
    else:
      # vmapped function had a scalar which with nonscalar args
      assert np.ndim(which) == 1
      which = broadcast_in_dim(which, cases[0].shape, [which_bdim],
                               out_sharding=typeof(cases[0]).sharding)
      return select_n(which, *cases), which_bdim
  elif np.ndim(which) == 0 and all(bdim is not None for bdim in case_bdims):
    if all(case_bdims[0] == bdim for bdim in case_bdims[1:]):
      return select_n(which, *cases), case_bdims[0]
    elif all(np.shape(cases[0]) == np.shape(c) for c in cases):
      bdim = case_bdims[0]
      other_cases = [batching.moveaxis(c, c_bdim, bdim)
                     for c, c_bdim in zip(cases[1:], case_bdims[1:])]
      return select_n(which, cases[0], *other_cases), bdim

  which = (batching.bdim_at_front(which, which_bdim, size,
                                  axis_data.explicit_mesh_axis)
           if np.shape(which) else which)
  if not all(() == np.shape(c) for c in cases):
    cases = [batching.bdim_at_front(c, bdim, size, axis_data.explicit_mesh_axis)
             for c, bdim in zip(cases, case_bdims)]
  assert all(np.shape(cases[0]) == np.shape(c) for c in cases[1:])
  if 0 < np.ndim(which) < np.ndim(cases[0]):
    # vmapped function had a scalar which with nonscalar args
    assert np.ndim(which) == 1
    which = broadcast_in_dim(which, cases[0].shape, [0],
                             out_sharding=typeof(cases[0]).sharding)
  if np.ndim(which) > np.ndim(cases[0]):
    assert np.ndim(cases[0]) == 0
    cases = [broadcast_like(c, which) for c in cases]
  return select_n(which, *cases), 0

