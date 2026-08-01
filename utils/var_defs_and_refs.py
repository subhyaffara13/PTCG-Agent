
def var_defs_and_refs(jaxpr: core.Jaxpr):
  defs: dict[core.Var, MaybeEqn] = {}
  refs: dict[core.Var, list[MaybeEqn]] = {}

  def read(a: core.Atom, eqn: MaybeEqn):
    if not isinstance(a, core.Literal):
      assert a in defs, a
      assert a in refs, a
      refs[a].append(eqn)

  def write(v: core.Var, eqn: MaybeEqn):
    assert v not in defs, v
    assert v not in refs, v
    if not isinstance(v, core.DropVar):
      defs[v] = eqn
      refs[v] = []

  for v in jaxpr.constvars:
    write(v, None)
  for v in jaxpr.invars:
    write(v, None)

  for eqn in jaxpr.eqns:
    for a in eqn.invars:
      read(a, eqn)
    for v in eqn.outvars:
      write(v, eqn)

  for a in jaxpr.outvars:
    read(a, None)

  res = [(v, defs[v], refs[v]) for v in defs]
  subs = map(var_defs_and_refs, core.subjaxprs(jaxpr))
  return [(jaxpr, res), *subs] if subs else (jaxpr, res)

