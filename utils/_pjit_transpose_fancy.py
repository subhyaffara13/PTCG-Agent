
def _pjit_transpose_fancy(
    cts_in, *args, jaxpr, in_shardings, out_shardings, in_layouts,
    out_layouts, donated_invars, ctx_mesh, name, keep_unused, inline,
    compiler_options_kvs):
  primals_ctrefs, specs = ad.project_accums(args)
  in_flat, in_tree = tree_flatten((primals_ctrefs, cts_in))
  in_avals = [core.AvalQDD(a, cur_qdd(x)) if (a := typeof(x)).has_qdd
              else a for x in in_flat]
  trans_jaxpr, out_tree = _transpose_jaxpr_fancy(jaxpr, in_tree, (*in_avals,), specs)

  trans_in_shardings = (
      [s for x, s in zip(args, in_shardings)
       if not isinstance(x, (ad.ValAccum, ad.NullAccum))] +
      [s for x, s in zip(cts_in, out_shardings) if not isinstance(x, ad.Zero)])
  trans_in_layouts = (
      [l for x, l in zip(args, in_layouts)
       if not isinstance(x, (ad.ValAccum, ad.NullAccum))] +
      [l for x, l in zip(cts_in, out_layouts) if not isinstance(x, ad.Zero)])
  cts_out_ = tree_unflatten(out_tree, trans_jaxpr.out_avals)
  trans_out_shardings = tuple(s for x, s in zip(cts_out_, in_shardings)
                              if isinstance(x, core.AbstractValue))
  trans_out_layouts   = tuple(l for x, l in zip(cts_out_, in_layouts  )
                              if isinstance(x, core.AbstractValue))

  try:
    cts_out = jit_p.bind(
        *in_flat, jaxpr=trans_jaxpr, in_shardings=tuple(trans_in_shardings),
        in_layouts=tuple(trans_in_layouts), out_shardings=trans_out_shardings,
        out_layouts=trans_out_layouts, donated_invars=(False,) * len(in_flat),
        ctx_mesh=ctx_mesh, name=name, keep_unused=keep_unused, inline=inline,
        compiler_options_kvs=compiler_options_kvs)
  except api_util.InternalFloatingPointError as e:
    print("Invalid nan value encountered in the backward pass of a jax.jit "
          "function. Calling the de-optimized backward pass.")
    try:
      ad.backward_pass3(jaxpr.jaxpr, False, jaxpr.consts, args, cts_in)
    except (FloatingPointError, ZeroDivisionError) as e2:
      raise e2 from None  # great
    else:
      # If control reaches this line, we got a NaN on the output of `compiled`
      # but not `fun.call_wrapped` on the same arguments. Let's tell the user.
      api_util._raise_no_nan_in_deoptimized(e)

  # pyrefly: ignore[unbound-name]  # pyrefly#2219
  for x, ct in zip(args, tree_unflatten(out_tree, cts_out)):
    if isinstance(x, ad.ValAccum): x.accum(ct)

