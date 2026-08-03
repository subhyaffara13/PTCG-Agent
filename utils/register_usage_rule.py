from typing import Any, Callable

def register_usage_rule(
    prim: core.Primitive,
) -> Callable[[Any], UsageRuleFn]:

  def wrapper(
      f: UsageRuleFn,
  ) -> UsageRuleFn:
    usage_rules[prim] = f
    return f

  return wrapper

