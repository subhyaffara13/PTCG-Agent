
def eval_sparse(
    jaxpr: core.Jaxpr,
    consts: Sequence[Array],  # all consts are dense
    spvalues: Sequence[SparsifyValue],  # mix of sparse and dense pointers into spenv
    spenv: SparsifyEnv,
) -> Sequence[SparsifyValue]:
  env : dict[core.Var, SparsifyValue] = {}

  def read(var: core.Atom) -> SparsifyValue:
    # all literals are dense
    if isinstance(var, core.Literal):
      return spenv.dense(var.val)
    else:
      assert isinstance(var, core.Var)
      return env[var]

  def write_buffer(var: core.Var, a: Array) -> None:
    if isinstance(var, core.DropVar):
      return
    env[var] = spenv.dense(a)

  def write(var: core.Var, a: SparsifyValue | None) -> None:
    if isinstance(var, core.DropVar):
      return
    assert a is not None
    env[var] = a

  safe_map(write_buffer, jaxpr.constvars, consts)
  safe_map(write, jaxpr.invars, spvalues)

  for eqn in jaxpr.eqns:
    prim = eqn.primitive
    invals = safe_map(read, eqn.invars)
    if any(val.is_bcsr() for val in invals):
      if prim not in sparse_rules_bcsr:
        _raise_unimplemented_primitive(prim)
      out = sparse_rules_bcsr[prim](spenv, *invals, **eqn.params)
    elif any(val.is_bcoo() for val in invals):
      if prim not in sparse_rules_bcoo:
        _raise_unimplemented_primitive(prim)
      out = sparse_rules_bcoo[prim](spenv, *invals, **eqn.params)
    else:
      out_bufs = prim.bind(*(spenv.data(val) for val in invals), **eqn.params)
      out_bufs = out_bufs if prim.multiple_results else [out_bufs]
      out = []
      for buf, outvar in safe_zip(out_bufs, eqn.outvars):
        if isinstance(outvar, core.DropVar):
          out.append(None)
        else:
          out.append(spenv.dense(buf))
    safe_map(write, eqn.outvars, out)

  return safe_map(read, jaxpr.outvars)

