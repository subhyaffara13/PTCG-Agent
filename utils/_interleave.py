
def _interleave(a, b, dim=0):
    # https://stackoverflow.com/questions/60869537/how-can-i-interleave-5-pytorch-tensors
    if b_trunc := (a.shape[dim] == b.shape[dim] + 1):
        pad = (
            [0] * ((b.ndim - dim - 1) * 2 + 1)
            + [1]
            + [0] * (b.ndim * 2 - ((b.ndim - dim - 1) * 2 + 2))
        )
        b = torch.nn.functional.pad(b, pad)

    stacked = torch.stack([a, b], dim=dim + 1)
    interleaved = torch.flatten(stacked, start_dim=dim, end_dim=dim + 1)
    # pyrefly: ignore [unbound-name]
    if b_trunc:
        # TODO: find torch alternative for slice_along dim for torch.jit.script to work
        interleaved = aten.slice(interleaved, dim, 0, b.shape[dim] + a.shape[dim] - 1)
    return interleaved


def _interleave(xs, ys):
  assert len(xs) == len(ys)
  return [e for pair in zip(xs, ys) for l in pair for e in l]


def _interleave(a, b, axis):
  """Given two Tensors of static shape, interleave them along the first axis."""
  assert a.shape[axis] == b.shape[axis] or a.shape[axis] == b.shape[axis] + 1
  a_pad = [(0, 0, 0)] * a.ndim
  b_pad = [(0, 0, 0)] * b.ndim
  a_pad[axis] = (0, 1 if a.shape[axis] == b.shape[axis] else 0, 1)
  b_pad[axis] = (1, 0 if a.shape[axis] == b.shape[axis] else 1, 1)
  op = lax.bitwise_or if a.dtype == np.bool_ else lax.add
  return op(lax.pad(a, lax._const(a, 0), a_pad),
            lax.pad(b, lax._const(b, 0), b_pad))

