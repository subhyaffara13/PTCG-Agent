import itertools

def dot_general_transpose_lhs(g, x, y, *, dimension_numbers, precision,
                              preferred_element_type: DTypeLike | None,
                              swap_ans=False):
  def _remaining(original, *removed_lists):
    removed = set(itertools.chain(*removed_lists))
    return [i for i in original if i not in removed]

  def _ranges_like(*xs):
    start = 0
    for x in xs:
      x_len = len(x)
      yield range(start, start + x_len)
      start += x_len

  (x_contract, y_contract), (x_batch, y_batch) = dimension_numbers
  x_ndim = x.aval.ndim
  x_kept = _remaining(range(x_ndim), x_contract, x_batch)
  y_kept = _remaining(range(np.ndim(y)), y_contract, y_batch)
  if swap_ans:
    ans_batch, ans_y, _ = _ranges_like(x_batch, y_kept, x_kept)
  else:
    ans_batch, _, ans_y = _ranges_like(x_batch, x_kept, y_kept)
  dims = ((ans_y, y_kept), (ans_batch, y_batch))
  x_contract_sorted_by_y = list(np.take(x_contract, np.argsort(y_contract)))
  out_axes = np.argsort(list(x_batch) + x_kept + x_contract_sorted_by_y)
  x_bar = lax.transpose(
    lax.dot_general(
      g, y, dims, precision=precision,
      preferred_element_type=preferred_element_type
    ),
    tuple(out_axes)
  )
  return x_bar

