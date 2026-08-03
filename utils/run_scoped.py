from typing import Any, Callable

def run_scoped(
    f: Callable[..., Any],
    *types: Any,
    collective_axes: Hashable | tuple[Hashable, ...] = (),
    **kw_types: Any,
) -> Any:
  """Calls the function with allocated references and returns the result.

  The positional and keyword arguments describe which reference types
  to allocate for each argument. Each backend has its own set of reference
  types in addition to :class:`jax.experimental.pallas.MemoryRef`.

  When ``collective_axes`` is specified, the same allocation will be returned for
  all programs that only differ in their program ids along the collective axes.
  It is an error not to call the same ``run_scoped`` in all programs along that
  axis.
  """
  if not isinstance(collective_axes, tuple):
    collective_axes = (collective_axes,)
  flat_types, in_tree = tree_util.tree_flatten((types, kw_types))
  flat_fun, out_tree_thunk = api_util.flatten_fun(
      lu.wrap_init(f,
                   debug_info=api_util.debug_info("pallas run_scoped",
                                                  f, types, kw_types)),
      in_tree)
  # We allow ref avals to be transformed references.
  ref_avals = [t.get_ref_aval() for t in flat_types]
  avals = [
      t.ref if isinstance(t, state_types.TransformedRef) else t
      for t in ref_avals
  ]
  # Note that only a subset of all transforms can be found here, and they are
  # never expected to contain any arrays.
  ref_transforms = tuple(
      t.transforms if isinstance(t, state_types.TransformedRef) else ()
      for t in ref_avals
  )
  flat_fun = wrap_with_transforms(flat_fun, ref_transforms)
  # Turn the function into a jaxpr. The body of run_scoped may have
  # effects (IO) on constvars (i.e. variables inherited from the
  # parent scope). Jax can't reason about effects to references that
  # are not in the invars of an operation so we just put them all
  # there.
  with config.mutable_array_checks(False):
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(flat_fun, avals)
  out = run_scoped_p.bind(*consts,
                          jaxpr=jaxpr,
                          collective_axes=collective_axes,
                          ref_transforms=ref_transforms)
  return tree_util.tree_unflatten(out_tree_thunk(), out)

