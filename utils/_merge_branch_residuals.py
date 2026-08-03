import itertools

def _merge_branch_residuals(branch_res_avals):
  def enumerate_equal(xs):
    counts = {v: itertools.count() for v in set(xs)}
    return [(x, next(counts[x])) for x in xs]
  branch_res_tagged_avals = map(enumerate_equal, branch_res_avals)
  all_tagged_avals = _ordered_unique(util.concatenate(branch_res_tagged_avals))
  indices = {v: i for i, v in enumerate(all_tagged_avals)}
  branch_indices = [
      [indices[aval] for aval in avals] for avals in branch_res_tagged_avals]
  all_avals = [x for x, _ in all_tagged_avals]
  return all_avals, branch_indices

