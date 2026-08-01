
def register_push_block_spec_rule(
    prim: core.Primitive,
) -> Callable[[Any], PushBlockSpecRuleFn]:

  def wrapper(
      f: PushBlockSpecRuleFn,
  ) -> PushBlockSpecRuleFn:
    push_block_spec_rules[prim] = f
    return f

  return wrapper

