
def _scan_transpose_fancy(cts, *args, reverse, length, num_consts,
                          num_carry, jaxpr, unroll):
  linear = [isinstance(x, ad.GradAccum) for x in args]
  consts_lin, init_lin, xs_lin = split_list(linear, [num_consts, num_carry])
  num_ires = len(consts_lin) - sum(consts_lin)

  # Rearrange jaxpr binders to separate out refs since we in/out swap pure vals:
  #   Before: [ires,               T d, T c,               T a, eres] -> [T c, T b]
  #   After:  [ires, T d_mut, T d_pure, T c, T a_mut, T a_pure, eres] -> [T c, T b]
  # where
  #   * `ires` means intensive (not scanned over / const) residuals, all Arrays;
  #   * `T d` means the intensive tangents, each a linear GradAccum or nonlinear
  #     plumbing ref or linear (zero) Array;
  #   * `T c` means the carry tangents;
  #   * `T a` means the extensive (scanned over) input tangents;
  #   * `eres` means the extensive residuals;
  #   * `T b` means the extensive tangent outputs.
  ires, consts_dot, carry_dot, xs_dot, eres = split_list(
      args, [num_ires, num_consts - num_ires, num_carry, sum(xs_lin)])
  is_mutable = [isinstance(x, ad.RefAccum) or not isinstance(x, ad.GradAccum)
                and isinstance(typeof(x), AbstractRef) for x in consts_dot]
  immut_consts_dot, mut_consts_bar = partition_list(is_mutable, consts_dot)
  jaxpr = _rearrange_mutable_binders(jaxpr, num_ires, num_consts - num_ires)
  is_mutable_ = [isinstance(x, ad.RefAccum) or not isinstance(x, ad.GradAccum)
                 and isinstance(typeof(x), AbstractRef) for x in xs_dot]
  immut_xs_dot, mut_xs_bar = partition_list(is_mutable_, xs_dot)
  jaxpr = _rearrange_mutable_binders(jaxpr, num_consts + num_carry, sum(xs_lin))
  del consts_dot, xs_dot, args

  # prepare cotangent values to be passed in to transpose
  ct_carry, ct_ys = split_list(cts, [num_carry])
  ct_carry = _map(ad.instantiate_zeros, ct_carry)  # TODO(mattjj): fixpoint

  # initialize values to be used to accumulate pure constant gradients
  immut_const_avals = jaxpr.in_avals[num_ires+len(mut_consts_bar):num_consts]
  ct_immut_consts = _map(lambda a: ad_util.zeros_like_aval(a.to_ct_aval()),
                         immut_const_avals)

  # prepare transpose inputs, unboxing RefAccums while noting which are linear
  trans_in, trans_tree = tree_flatten([ires, mut_consts_bar, ct_immut_consts,
                                       ct_carry, mut_xs_bar, ct_ys, eres])
  lin_refs = tuple(isinstance(x, ad.RefAccum) for x in trans_in)
  trans_in = [x.inst().ref if l else x for l, x in zip(lin_refs, trans_in)]

  # prepare transposed jaxpr
  accum_typeof = lambda x: (x.aval if isinstance(x, ad.GradAccum)
                            else core.aval_qdd_from_current_val(typeof(x), x))
  trans_avals, ext_avals = split_list(_map(accum_typeof, trans_in), [num_consts+num_carry])
  trans_avals = trans_avals + [core.mapped_leading_aval(length, a) for a in ext_avals]
  xs_avals = tuple(core.mapped_leading_aval(length, accum_typeof(x)) for x in immut_xs_dot)
  jaxpr_trans = _transpose_scan_jaxpr_fancy(
      jaxpr, trans_tree, tuple(trans_avals), lin_refs, xs_avals)

  # run it
  outs = scan_p.bind(
      *trans_in, reverse=not reverse, length=length, jaxpr=jaxpr_trans,
      num_consts=num_ires + len(mut_consts_bar),
      num_carry=len(immut_consts_dot) + len(carry_dot), unroll=unroll)

  for a, x in zip([*immut_consts_dot, *carry_dot, *immut_xs_dot], outs):
    if isinstance(a, ad.GradAccum): a.accum(x)

