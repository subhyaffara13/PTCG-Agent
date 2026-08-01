
def register_cost_rule(primitive: jax_core.Primitive, rule):
  _cost_rules[primitive] = rule

