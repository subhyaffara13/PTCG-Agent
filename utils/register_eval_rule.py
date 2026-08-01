
def register_eval_rule(
    prim: core.Primitive,
) -> Callable[[Any], EvalRuleFn]:
  def wrapper(
      f: EvalRuleFn,
  ) -> EvalRuleFn:
    eval_rules[prim] = f
    return f

  return wrapper

