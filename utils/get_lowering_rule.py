
def get_lowering_rule(params_cls, expected_platform: str):
  rule_info = _backend_lowering_rules.get(params_cls)
  if rule_info is None:
    return None
  rule, platform = rule_info
  if platform != expected_platform:
    raise ValueError(
        f"Compiler params for platform {platform} cannot be used for"
        f" {expected_platform} lowering."
    )
  return rule

