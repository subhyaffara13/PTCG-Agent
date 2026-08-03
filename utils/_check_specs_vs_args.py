from typing import Callable

def _check_specs_vs_args(
    f: Callable, mesh: Mesh | AbstractMesh, in_tree: PyTreeDef, in_specs: Specs,
    dyn_argnums: Sequence[int], in_specs_flat: Sequence[P],
    xs: Sequence) -> None:
  in_avals = map(core.shaped_abstractify, xs)
  fail = [a if isinstance(p, P) and len(p) > a.ndim else no_fail
          for p, a in zip(in_specs_flat, in_avals)]
  if any(f is not no_fail for f in fail):
    fail = _expand_fail(in_tree, dyn_argnums, fail)
    msg = _spec_rank_error(SpecErrorType.input, f, in_tree, in_specs, fail)
    raise ValueError(msg)
  bad = lambda a, d, ns: a.shape[d] % prod(mesh.shape[n] for n in ns)
  fail = [a if (isinstance(s, P) and
                any(bad(a, d, ns) for d, ns in _spec_to_names(s).items()))
          else no_fail for a, s in zip(in_avals, in_specs_flat)]
  if any(f is not no_fail for f in fail):
    fail = _expand_fail(in_tree, dyn_argnums, fail)
    msg = _spec_divisibility_error(f, mesh, in_tree, in_specs, fail)
    raise ValueError(msg)

