
def _linear_solve_batching_rule(axis_data, args, dims, const_lengths, jaxprs):
  orig_bat = [d is not None for d in dims]

  params, b = _split_linear_solve_args(args, const_lengths)
  params_dims, b_dims = _split_linear_solve_args(dims, const_lengths)
  params_bat, orig_b_bat = _split_linear_solve_args(orig_bat, const_lengths)

  (matvec, vecmat, solve, solve_t) = jaxprs
  (matvec_bat, vecmat_bat, solve_bat, solve_t_bat) = params_bat

  # number of operator out avals is assumed to be the same for matvec/vecmat
  num_operator_out_avals = len(matvec.out_avals)
  num_aux = len(solve.out_avals) - num_operator_out_avals
  # Fixpoint computation of which parts of x and b are batched; we need to
  # ensure this is consistent between all four jaxprs
  b_bat = orig_b_bat
  x_bat = [False] * len(solve.out_avals)
  for i in range(1 + len(orig_b_bat) + len(solve.out_avals)):
    # Apply vecmat and solve -> new batched parts of x
    solve_jaxpr_batched, solve_x_bat = batching.batch_jaxpr(
        solve, axis_data, solve_bat + b_bat, instantiate=x_bat)
    if vecmat is None:
      vecmat_jaxpr_batched = None
      x_bat_out = solve_x_bat
    else:
      vecmat_jaxpr_batched, vecmat_x_bat = batching.batch_jaxpr(
          vecmat, axis_data, vecmat_bat + b_bat, instantiate=b_bat)
      # batch all aux data by default
      x_bat_out = _map(operator.or_, vecmat_x_bat + [True] * num_aux, solve_x_bat)
    # keep a slice of only the linear operator part of solve's avals
    x_bat_noaux = x_bat_out[:num_operator_out_avals]

    # Apply matvec and solve_t -> new batched parts of b
    matvec_jaxpr_batched, matvec_b_bat = batching.batch_jaxpr(
        matvec, axis_data, matvec_bat + x_bat_noaux, instantiate=b_bat)
    if solve_t is None:
      solve_t_jaxpr_batched = None
      b_bat_out = _map(operator.or_, matvec_b_bat, orig_b_bat)
    else:
      solve_t_jaxpr_batched, solve_t_b_aux_bat = batching.batch_jaxpr(
          solve_t, axis_data, solve_t_bat + x_bat_noaux, instantiate=x_bat_out)
      assert len(solve_t_b_aux_bat) == len(orig_b_bat) + num_aux
      solve_t_b_bat, _ = split_list(solve_t_b_aux_bat, [len(orig_b_bat)])
      b_bat_out = _map(lambda m, s, o: m or s or o, matvec_b_bat, solve_t_b_bat,
                      orig_b_bat)
    if x_bat_out == x_bat and b_bat_out == b_bat:
      break
    else:
      x_bat = x_bat_out
      b_bat = b_bat_out
  else:
    assert False, "Fixedpoint not reached"

  batched_jaxprs = _LinearSolveTuple(matvec_jaxpr_batched, vecmat_jaxpr_batched,
                                     solve_jaxpr_batched, solve_t_jaxpr_batched)

  # Move batched axes to the front
  new_params = [
      batching.moveaxis(x, d, 0)
      if d is not None and d != 0 else x
      for x, d in zip(_flatten(params), _flatten(params_dims))
  ]
  # Broadcast out b if necessary
  new_b = [
      batching.broadcast(x, axis_data.size, 0, axis_data.explicit_mesh_axis)
      if now_bat and not was_bat else
      batching.moveaxis(x, d, 0) if now_bat and d != 0 else x
      for x, d, was_bat, now_bat in zip(b, b_dims, orig_b_bat, b_bat)
  ]

  outs = linear_solve_p.bind(
      *(new_params + new_b),
      const_lengths=const_lengths,
      jaxprs=batched_jaxprs)
  out_dims = [0 if batched else None for batched in solve_x_bat]
  return outs, out_dims

