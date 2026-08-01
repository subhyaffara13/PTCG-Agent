
def _dot_general_usage_rule(
    ctx: UsageRuleContext, used_out: set[Usage], **params
):
  del ctx, params
  if Usage.REGULAR in used_out:
    return [{Usage.REGULAR}, {Usage.REGULAR}]
  return [set(), set()]

