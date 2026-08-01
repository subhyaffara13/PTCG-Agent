
def _tridiagonal_solve_batching_rule(
    batched_args, batch_dims, *, perturb_singular):
  dl, d, du, b = batched_args
  bdl, bd, bdu, bb = batch_dims
  if (bdl is None and
      bd is None and
      bdu is None):

    b = batching.moveaxis(b, bb, -2)
    b_flat = b.reshape(b.shape[:-3]  + (b.shape[-3], b.shape[-2] * b.shape[-1]))
    bdim_out = b.ndim - 2
    out_flat = tridiagonal_solve(dl, d, du, b_flat,
                                 perturb_singular=perturb_singular)
    return out_flat.reshape(b.shape), bdim_out
  else:
    size = next(t.shape[i] for t, i in zip(batched_args, batch_dims)
                if i is not None)
    dl = batching.bdim_at_front(dl, bdl, size)
    d = batching.bdim_at_front(d, bd, size)
    du = batching.bdim_at_front(du, bdu, size)
    b = batching.bdim_at_front(b, bb, size)
    return tridiagonal_solve(dl, d, du, b, perturb_singular=perturb_singular), 0

