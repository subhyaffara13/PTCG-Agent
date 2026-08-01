
def forward(model, x):
  return model(x)


def forward(model, x: chex.Array) -> chex.Array:
  return model(x)


def forward(model: rcfr.DeepRcfrModel, x: chex.Array) -> chex.Array:
  """Batched call for the flax.nnx model."""
  return model(x)

