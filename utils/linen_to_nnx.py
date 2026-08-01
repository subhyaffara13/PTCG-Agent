
def linen_to_nnx(model: linen.Module, seed: int = 0) -> nnx.bridge.ToNNX:
  # NOTE: could be issues with handling_randomness
  model = nnx.bridge.ToNNX(model, rngs=nnx.Rngs(seed))
  return model

