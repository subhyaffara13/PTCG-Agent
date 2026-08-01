
def register_default_eval_rule(prim: core.Primitive):
  def default_rule(ctx, *args, **params):
    assert all(bs is pallas_core.no_block_spec for bs in ctx.out_block_specs)
    return prim.bind(*args, **params)

  register_eval_rule(prim)(default_rule)

