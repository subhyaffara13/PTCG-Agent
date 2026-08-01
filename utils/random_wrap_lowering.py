
def random_wrap_lowering(ctx, base_arr, *, impl):
  return [base_arr]


def random_wrap_lowering(ctx: LoweringRuleContext, key_data, *, impl):
  del ctx
  if not pl_random.is_pallas_impl(impl):
    return key_data
  raise ValueError(
      "wrap_key_data not support for Pallas PRNG keys. Use"
      " wrap_pallas_seed instead."
  )

