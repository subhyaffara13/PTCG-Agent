import functools

def register_eltwise_rule(prim: core.Primitive):
  register_pull_block_spec_rule(prim)(
      functools.partial(_eltwise_pull_rule, prim)
  )
  register_usage_rule(prim)(functools.partial(_eltwise_usage_rule, prim))
  register_eval_rule(prim)(functools.partial(_eltwise_eval_rule, prim))
  register_push_block_spec_rule(prim)(
      functools.partial(_eltwise_push_rule, prim)
  )

