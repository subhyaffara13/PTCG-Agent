
def lift_jvp(num_errs: int, num_consts: int,
             jvp_jaxpr_fun: lu.WrappedFun) -> lu.WrappedFun:
  def jvp(*xs):
    n, ragged = divmod(len(xs), 2)
    assert not ragged
    primals, tangents = xs[num_consts+num_errs:n], xs[n+num_consts+num_errs:]
    zeros = [type(t) is SymbolicZero for t in tangents]
    jvp_jaxpr, jvp_consts, out_zeros = jvp_jaxpr_fun.call_wrapped(*zeros)
    nonzero_tangents = [t for t in tangents if type(t) is not SymbolicZero]
    out = core.eval_jaxpr(jvp_jaxpr, jvp_consts, *primals, *nonzero_tangents)
    out_primals, nz_out_tangents = split_list(out, [len(out_zeros)])
    nz_out_tangents_ = iter(nz_out_tangents)
    out_tangents = [SymbolicZero(core.typeof(p).to_tangent_aval())
                    if z else next(nz_out_tangents_)
                    for p, z in zip(out_primals, out_zeros)]
    assert next(nz_out_tangents_, None) is None
    primal_errs = xs[num_consts:num_consts+num_errs]
    tangent_errs = xs[n+num_consts:n+num_consts+num_errs]
    return [*primal_errs, *out_primals, *tangent_errs, *out_tangents]
  return lu.wrap_init(jvp, debug_info=jvp_jaxpr_fun.debug_info)


def lift_jvp(num_consts: int, jvp_jaxpr_fun: lu.WrappedFun) -> lu.WrappedFun:
  def jvp(*xs):
    n, ragged = divmod(len(xs), 2)
    assert not ragged
    primals, tangents = xs[num_consts:n], xs[n+num_consts:]
    zeros = [type(t) is SymbolicZero for t in tangents]
    jvp_jaxpr, jvp_consts, out_zeros = jvp_jaxpr_fun.call_wrapped(*zeros)
    nonzero_tangents = [t for t in tangents if type(t) is not SymbolicZero]
    out = core.eval_jaxpr(jvp_jaxpr, jvp_consts, *primals, *nonzero_tangents)
    out_primals, nz_out_tangents = split_list(out, [len(out_zeros)])
    nz_out_tangents_ = iter(nz_out_tangents)
    out_tangents = [SymbolicZero(core.typeof(p).to_tangent_aval())
                    if z else next(nz_out_tangents_)
                    for p, z in zip(out_primals, out_zeros)]
    assert next(nz_out_tangents_, None) is None
    return [*out_primals, *out_tangents]
  return lu.wrap_init(jvp, debug_info=jvp_jaxpr_fun.debug_info)

