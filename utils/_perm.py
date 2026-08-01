
def _perm(primal_counts: Sequence[int], tangent_counts: Sequence[int],
          lst: Sequence[Any]) -> Sequence[Any]:
  n = sum(primal_counts)
  primals, tangents = lst[:n], lst[n:]
  primal_groups = split_list(primals, primal_counts[:-1])
  tangent_groups = split_list(tangents, tangent_counts[:-1])
  return _interleave(primal_groups, tangent_groups)

