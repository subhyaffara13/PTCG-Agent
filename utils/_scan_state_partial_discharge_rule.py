
def _scan_state_partial_discharge_rule(
    should_discharge, in_avals, out_avals, *args, jaxpr, num_consts, num_carry,
    unroll, reverse, length):
  # jaxpr: [*consts, *pure_carry, *xs] -> [*pure_carry, *pure_ys]
  # jaxpr_: [*consts, *pure_carry, *xs] -> [*pure_carry, *pure_ys, *ref_outs]
  discharged_jaxpr = state_discharge.discharge_state(
      jaxpr, should_discharge=should_discharge)

  num_xs = len(args) - num_consts - num_carry
  is_ref = [isinstance(a, AbstractRef) and s for a, s in zip(jaxpr.in_avals, should_discharge)]
  is_ref_const, _, is_ref_xs = split_list_checked(is_ref, [num_consts, num_carry, num_xs])
  num_const_refs = sum(is_ref_const)
  num_xs_refs = sum(is_ref_xs)
  num_pure_consts = num_consts - num_const_refs
  num_ys = len(jaxpr.out_avals) - num_carry

  ds = partial(slicing.dynamic_index_in_dim, keepdims=False, allow_negative_indices=False)
  dus = partial(slicing.dynamic_update_index_in_dim, axis=0, allow_negative_indices=False)

  def body(*consts_carry_xs):
    pure_consts, [i_], const_refvals, carry, xs_refvals_, pure_xs = split_list(
        consts_carry_xs, [num_pure_consts, 1, num_const_refs, num_carry, num_xs_refs])
    i = length - i_ - 1 if reverse else i_
    xs_refvals = [ds(x, i) for x in xs_refvals_]
    consts = merge_lists(is_ref_const, pure_consts, const_refvals)
    xs = merge_lists(is_ref_xs, pure_xs, xs_refvals)
    outs = eval_jaxpr_p.bind(*consts, *carry, *xs, jaxpr=discharged_jaxpr)
    carry, ys, const_refvals, xs_updates = split_list_checked(
        outs, [num_carry, num_ys, num_const_refs, num_xs_refs])
    xs_refvals = [dus(x, u, i) for x, u in zip(xs_refvals_, xs_updates)]
    return [i_ + 1, *const_refvals, *carry, *xs_refvals, *ys]

  def rearrange(lst):
    consts, carry, xs = split_list_checked(lst, [num_consts, num_carry, num_xs])
    pure_consts, ref_consts = partition_list(is_ref_const, consts)
    pure_xs, ref_xs = partition_list(is_ref_xs, xs)
    return *pure_consts, *ref_consts, *carry, *ref_xs, *pure_xs

  in_avals = rearrange([core.typeof(a) for a in args])
  pure_const_avals, carry_avals, pure_xs_avals = split_list(
      in_avals, [num_pure_consts, num_const_refs + num_carry + num_xs_refs])
  pure_x_avals = [core.mapped_leading_aval(length, a) for a in pure_xs_avals]
  in_avals = [*pure_const_avals, core.typeof(0), *carry_avals, *pure_x_avals]

  if jaxpr.jaxpr.debug_info.arg_names is None:
    arg_names = None
  else:
    arg_names = rearrange(jaxpr.jaxpr.debug_info.arg_names)
    pure_const_names, carry_names, pure_xs_names = split_list(
        arg_names, [num_pure_consts, num_const_refs + num_carry + num_xs_refs])
    arg_names = (*pure_const_names, 'iter', *carry_names, *pure_xs_names)

  dbg = jaxpr.jaxpr.debug_info._replace(arg_names=arg_names, result_paths=None)

  new_jaxpr, _ = pe.trace_to_jaxpr(body,
      FlatTree.flatten_args(*in_avals),
      debug_info=dbg)

  pure_consts, carry, pure_xs = split_list(
      rearrange(args), [num_pure_consts, num_const_refs + num_carry + num_xs_refs])
  _, *outs = scan_p.bind(
      *pure_consts, 0, *carry, *pure_xs, jaxpr=new_jaxpr, length=length,
      unroll=unroll, reverse=reverse, num_consts=num_pure_consts,
      num_carry=1 + num_const_refs + num_carry + num_xs_refs)

  const_refvals, carry, xs_refvals, ys = split_list(
      outs, [num_const_refs, num_carry, num_xs_refs])
  refvals_iter = it.chain(const_refvals, xs_refvals)
  refvals_out = [next(refvals_iter) if r else None for r in is_ref]
  assert next(refvals_iter, None) is None
  return refvals_out, [*carry, *ys]

