
def _roofline_interpreter(
  f_name: str,
  jaxpr: core.Jaxpr,
  mesh: Mesh | AbstractMesh | None,
  *,
  pin_lhs_in_vmem: bool = False,
  pin_rhs_in_vmem: bool = False,
) -> RooflineResult:
  name_stack = source_info_util.new_name_stack(util.wrap_name("roofline", f_name))

  result = RooflineResult.zeros()

  env: dict[core.Var, RooflineShape] = {}

  def write(v: core.Var, node: RooflineShape):
    assert node is not None
    env[v] = node

  def read(v: core.Atom) -> RooflineShape:
    if type(v) is core.Literal:
      return RooflineShape.from_aval(core.typeof(v.val))
    else:
      assert isinstance(v, core.Var)
      return env[v]

  def aval(v: core.Atom) -> core.AbstractValue:
    if type(v) is core.Literal:
      return core.typeof(v.val)
    else:
      return v.aval

  def sum_bytes(shapes: Sequence[RooflineShape]) -> int:
    return sum(shape.bytes for shape in shapes)

  jaxpr = jaxpr.jaxpr if isinstance(jaxpr, core.ClosedJaxpr) else jaxpr
  make_roofline_shape = lambda x: RooflineShape.from_aval(aval(x))
  foreach(
    write,
    jaxpr.constvars,
    map(make_roofline_shape, jaxpr.constvars),
  )
  foreach(write, jaxpr.invars, map(make_roofline_shape, jaxpr.invars))
  last_used = core.last_used(jaxpr)

  current_hbm_bytes = sum_bytes(list(env.values()))
  peak_hbm_bytes = current_hbm_bytes

  for eqn in jaxpr.eqns:
    source_info = eqn.source_info.replace(
      name_stack=name_stack + eqn.source_info.name_stack
    )
    with source_info_util.user_context(
      eqn.source_info.traceback, name_stack=source_info.name_stack
    ):
      if "jaxpr" in eqn.params:
        result += _roofline_interpreter(
          util.wrap_name(eqn.primitive.name, f_name),
          eqn.params["jaxpr"],
          mesh,
          pin_lhs_in_vmem=pin_lhs_in_vmem,
          pin_rhs_in_vmem=pin_rhs_in_vmem,
        )
      elif "call_jaxpr" in eqn.params:
        # Used for custom_jvp_call_p. Recursively calculates roofline result for
        # all primitives in the custom function.
        result += _roofline_interpreter(
          util.wrap_name(eqn.primitive.name, f_name),
          eqn.params['call_jaxpr'],
          mesh,
          pin_lhs_in_vmem=pin_lhs_in_vmem,
          pin_rhs_in_vmem=pin_rhs_in_vmem,
        )
      elif eqn.primitive not in _rooflines:
        msg = f"No roofline rule for {eqn.primitive}, skipping..."
        for attr in dir(eqn):
          if not attr.startswith("_"):
            msg += f"\n{attr}: {getattr(eqn, attr)}"
        logging.warning(msg)
      else:
        rule = _rooflines[eqn.primitive]
        result += rule(
          RooflineRuleContext(
            name_stack=source_info.name_stack,
            primitive=eqn.primitive,
            avals_in=map(aval, eqn.invars),
            avals_out=map(aval, eqn.outvars),
            jaxpr_eqn_ctx=eqn.ctx,
            mesh=mesh,
            pin_lhs_in_vmem=pin_lhs_in_vmem,
            pin_rhs_in_vmem=pin_rhs_in_vmem,
          ),
          *map(read, eqn.invars),
          **eqn.params,
        )

      # Add bytes for the newly-created output variables.
      outvar_shapes = map(make_roofline_shape, eqn.outvars)
      current_hbm_bytes += sum_bytes(outvar_shapes)
      foreach(write, eqn.outvars, outvar_shapes)

      # Remove bytes for the no-longer-needed input variables.
      removed_shapes = [
          env[v] for v in eqn.invars
          if not isinstance(v, core.Literal) and last_used[v] is eqn
      ]
      current_hbm_bytes -= sum_bytes(removed_shapes)
      core.clean_up_dead_vars(eqn, env, last_used)

      peak_hbm_bytes = max(peak_hbm_bytes, current_hbm_bytes)

  result += RooflineResult(peak_hbm_bytes=peak_hbm_bytes)
  return result

