
def random_bits_lowering(ctx, keys, *, bit_width, shape):
  aval, = ctx.avals_in
  impl = aval.dtype._impl
  bits = iterated_vmap_unary(
      aval.ndim, lambda k: impl.random_bits(k, bit_width, shape))
  bits_lowering = mlir.lower_fun(bits, multiple_results=False)
  ctx_new = ctx.replace(avals_in=[core.physical_aval(aval)])
  out = bits_lowering(ctx_new, keys)
  ctx.set_tokens_out(ctx_new.tokens_out)
  return out


def random_bits_lowering(ctx: LoweringRuleContext, keys, *, bit_width, shape):
  assert bit_width == 32, "Only 32-bit PRNG supported."
  aval, = ctx.avals_in
  assert isinstance(aval.dtype, prng.KeyTy)
  impl = aval.dtype._impl
  _proxy_fn = impl.random_bits
  if not pl_random.is_pallas_impl(impl):
    def new_lowering(key, bit_width, shape):
      key = jax.random.key_data(key).astype(jnp.uint32)
      return impl.random_bits(key, bit_width, shape)
    _proxy_fn = new_lowering
  bits_lowering = lower_fun(_proxy_fn)
  return bits_lowering(ctx, keys, bit_width=bit_width, shape=shape)

