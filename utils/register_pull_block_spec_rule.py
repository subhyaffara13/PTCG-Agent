from typing import Any, Callable

def register_pull_block_spec_rule(
    prim: core.Primitive,
) -> Callable[[Any], PullBlockSpecRuleFn]:

  def wrapper(
      f: PullBlockSpecRuleFn,
  ) -> PullBlockSpecRuleFn:
    pull_block_spec_rules[prim] = f
    return f

  return wrapper

