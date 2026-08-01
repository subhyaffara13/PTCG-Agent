
def _transpose_jaxpr(jaxpr, in_tree, in_avals):
  cell = lambda: None
  def transposed(*in_flat):
    primals_in, cts_in = tree_unflatten(in_tree, in_flat)
    primals_in = tuple(
        ad.UndefinedPrimal(p.aval.update(memory_space=core.MemorySpace.Any))
        if type(p) is ad.UndefinedPrimal else p for p in primals_in)
    cts_in = [ad.Zero(ct.aval.update(memory_space=core.MemorySpace.Any))
              if type(ct) is ad.Zero else ct for ct in cts_in]
    out = ad.backward_pass(jaxpr.jaxpr, False, jaxpr.consts, primals_in, cts_in)
    out = [ct if not isinstance(ct, ad.Zero) else None for ct in out]
    cts_out, cell.out_tree = tree_flatten(out)  # pyrefly: ignore[missing-attribute]
    return cts_out
  dbg = jaxpr.jaxpr.debug_info.with_unknown_names()
  trans_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(transposed, debug_info=dbg), in_avals)
  return core.ClosedJaxpr(trans_jaxpr, consts), cell.out_tree  # pyrefly: ignore[missing-attribute]


def _transpose_jaxpr(jaxpr, in_avals, in_tree):
  cell = lambda: None
  def transposed(*in_flat):
    primals_in, cts_in = tree_unflatten(in_tree, in_flat)
    out = ad.backward_pass(jaxpr.jaxpr, False, jaxpr.consts, primals_in, cts_in)
    out = [ct if not isinstance(ct, ad.Zero) else None for ct in out]
    cts_out, cell.out_tree = tree_flatten(out)  # pyrefly: ignore[missing-attribute]
    return cts_out
  dbg = jaxpr.jaxpr.debug_info.with_unknown_names()
  trans_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(transposed, debug_info=dbg), in_avals)
  return core.ClosedJaxpr(trans_jaxpr, consts), cell.out_tree  # pyrefly: ignore[missing-attribute]


def _transpose_jaxpr(jaxpr: core.ClosedJaxpr,
                     in_lin: Sequence[bool],
                     out_zeros: Sequence[bool]):
  in_avals = ([a for a,  lin in zip(jaxpr.in_avals,  in_lin   ) if not lin] +
              [a.to_ct_aval() for a, zero in zip(jaxpr.out_avals, out_zeros)
               if not zero])
  cell = lambda: None

  def transposed(*args_flat):
    ins_flat, out_cts_flat = split_list(args_flat, [len(in_lin) - sum(in_lin)])

    # Evaluate nonlinear parts using partial evaluation to get a linear jaxpr.
    # TODO(mattjj): revise not to require disabling checks
    with config.mutable_array_checks(False):
      jaxpr_rematted, lin_jaxpr, out_uk, res_avals = \
          pe.partial_eval_jaxpr_nounits(jaxpr, in_lin, False)
    with source_info_util.extend_name_stack('rematted_computation'):
      consts = core.jaxpr_as_fun(jaxpr_rematted)(*ins_flat)

    # Transpose the linear jaxpr (which only has linear inputs).
    out_cts_iter = iter(out_cts_flat)
    out_cts = [ad_util.Zero(aval.to_ct_aval()) if zero else next(out_cts_iter)
               for aval, zero in zip(jaxpr.out_avals, out_zeros)]
    assert next(out_cts_iter, None) is None
    dummy_args = [ad.UndefinedPrimal(aval.to_ct_aval())
                  for aval in lin_jaxpr.in_avals[len(consts):]]
    in_cts = ad.backward_pass(lin_jaxpr.jaxpr, False, lin_jaxpr.consts,
                              [*consts, *dummy_args], out_cts)
    in_cts = in_cts[len(consts):]

    # Identify symbolic zeros in the resulting cotangents, and return nonzeros.
    in_zeros = cell.in_cts_zero = [type(ct) is ad_util.Zero for ct in in_cts]  # pyrefly: ignore[missing-attribute]
    in_cts_nz, _ = partition_list(in_zeros, in_cts)
    return in_cts_nz

  dbg = jaxpr.jaxpr.debug_info.with_unknown_names()
  in_avals_flat_tree = FlatTree.flatten((tuple(in_avals), {}))
  transposed_closed_jaxpr, _ = pe.trace_to_jaxpr(
      transposed, in_avals_flat_tree, dbg)
  return transposed_closed_jaxpr, cell.in_cts_zero  # pyrefly: ignore[missing-attribute]


def _transpose_jaxpr(jaxpr, in_avals, in_tree):
  cell = lambda: None
  def transposed(*in_flat):
    primals_in, cts_in = tree_unflatten(in_tree, in_flat)
    out = ad.backward_pass(jaxpr.jaxpr, False, jaxpr.consts, primals_in, cts_in)
    out = [ct if not isinstance(ct, ad.Zero) else None for ct in out]
    cts_out, cell.out_tree = tree_flatten(out)  # pyrefly: ignore[missing-attribute]
    return cts_out
  dbg = jaxpr.jaxpr.debug_info.with_unknown_names()
  trans_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(transposed, debug_info=dbg), in_avals)
  return core.ClosedJaxpr(trans_jaxpr, consts), cell.out_tree  # pyrefly: ignore[missing-attribute]

