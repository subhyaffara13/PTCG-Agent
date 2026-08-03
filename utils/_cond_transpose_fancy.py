import functools

def _cond_transpose_fancy(cts_in, index, *args, branches, **params):
  assert not isinstance(index, ad.GradAccum)
  primals_ctrefs, specs = ad.project_accums(args)
  in_flat, in_tree = tree_flatten((primals_ctrefs, cts_in))
  in_avals = tuple(core.AvalQDD(a, cur_qdd(x)) if (a := typeof(x)).has_qdd
                   else a for x in in_flat)
  trans_branches, out_trees = unzip2(
      _transpose_jaxpr_fancy(j, in_tree, in_avals, specs, (False,) * len(args))
      for j in branches)
  out_nzs = [[not isinstance(x, ad.Zero) for x in tree_unflatten(t, j.out_avals)]
             for t, j in zip(out_trees, trans_branches)]
  out_nz = tuple(map(partial(functools.reduce, operator.or_), zip(*out_nzs)))
  trans_branches, out_trees = unzip2(
      _transpose_jaxpr_fancy(j, in_tree, in_avals, specs, out_nz) for j in branches)
  out_tree, = set(out_trees)
  cts_out = cond_p.bind(index, *in_flat, branches=(*trans_branches,), **params)
  for x, ct in zip(args, tree_unflatten(out_tree, cts_out)):
    if isinstance(x, ad.ValAccum): x.accum(ct)

