
def compute_usage(input_tokens: int, output_tokens: int) -> ResponseUsage:
    """Build a ``ResponseUsage`` object for a Responses API reply.

    Args:
        input_tokens (`int`): Number of prompt tokens.
        output_tokens (`int`): Number of generated tokens.

    Returns:
        `ResponseUsage`: Usage statistics with zero-filled detail fields.
    """
    return ResponseUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=input_tokens + output_tokens,
        input_tokens_details=InputTokensDetails(cached_tokens=0),
        output_tokens_details=OutputTokensDetails(reasoning_tokens=0),
    )


def compute_usage(jaxpr: core.Jaxpr, jaxpr_out_usages):
  # TODO(sharadmv): maybe simplify this by only identifying scalar prefetch
  # and then DCEing it out.
  usage_env: dict[core.Atom, set[Usage]] = {}

  def read_usage_env(atom: core.Atom) -> set[Usage]:
    assert not isinstance(atom, core.Literal)
    return usage_env.get(atom, {Usage.REGULAR})

  def write_usage_env(atom: core.Atom, usage: set[Usage]):
    if isinstance(atom, core.Literal):
      return
    if atom not in usage_env:
      usage_env[atom] = set()
    usage_env[atom] |= usage

  util.safe_map(write_usage_env, jaxpr.outvars, jaxpr_out_usages)

  for eqn in jaxpr.eqns[::-1]:
    out_usages = util.safe_map(read_usage_env, eqn.outvars)
    rule = usage_rules.get(eqn.primitive, None)
    if rule:
      usage_rule_ctx = UsageRuleContext(
          avals_in=tuple(v.aval for v in eqn.invars),
          avals_out=tuple(v.aval for v in eqn.outvars),
      )
      if eqn.primitive.multiple_results:
        in_usages = rule(usage_rule_ctx, out_usages, **eqn.params)
      else:
        in_usages = rule(usage_rule_ctx, out_usages[0], **eqn.params)
    else:
      # Usages are forwarded
      all_usages = set.union(*out_usages)
      in_usages = [all_usages] * len(eqn.invars)
    util.safe_map(write_usage_env, eqn.invars, in_usages)
  return read_usage_env

