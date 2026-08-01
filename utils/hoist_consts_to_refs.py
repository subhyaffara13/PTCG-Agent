
def hoist_consts_to_refs(
    jaxpr: core.Jaxpr,
    *,
    index: int = 0,
    make_abstract_ref: Callable[[core.AbstractValue], AbstractRef] = lambda aval: AbstractRef(aval)
) -> core.Jaxpr:
  """Hoists the constants in the given jaxpr into invars.

  Args:
    jaxpr: The jaxpr.
    index: The index where the invars for the constants should be inserted.
      By default, the new invars are inserted *before* any existing invars.
    make_abstract_ref: a callable to construct an AbstractRef, or subtype
      thereof, from a constant AbstractValue.

  Returns:
    A new jaxpr where the constants were hoisted into invars as ``Ref``s.
  """
  if not jaxpr.constvars:
    return jaxpr  # Nothing to hoist.

  is_const_ref = [
      isinstance(var.aval, AbstractRef) for var in jaxpr.constvars
  ]
  const_avals = [
      var.aval if is_ref else make_abstract_ref(var.aval)
      for is_ref, var in zip(is_const_ref, jaxpr.constvars)
  ]
  in_avals = [var.aval for var in jaxpr.invars]
  in_avals[index:index] = const_avals

  def _hoist(*consts_args):
    args0, all_consts, args1 = split_list(
        consts_args, [index, len(const_avals)]
    )
    # We immediately read the const values out of the `Ref`s.
    all_consts = [
        c if is_ref else ref_get(c, ())
        for is_ref, c in zip(is_const_ref, all_consts)
    ]
    return core.eval_jaxpr(jaxpr, all_consts, *args0, *args1)

  hoisted_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(_hoist, debug_info=jaxpr.debug_info.with_unknown_names()),
      in_avals)
  assert not consts, "All consts should have been converted to refs"
  return hoisted_jaxpr

