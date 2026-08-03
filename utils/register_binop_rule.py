import functools

def register_binop_rule(prim: core.Primitive):
  register_pull_block_spec_rule(prim)(functools.partial(_binop_pull_rule, prim))
  register_usage_rule(prim)(functools.partial(_binop_usage_rule, prim))
  register_eval_rule(prim)(functools.partial(_binop_eval_rule, prim))

