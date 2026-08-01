
def jax_train_step(
    graphdef: nn.GraphDef, state: nn.State, x: chex.Array, y: chex.Array
) -> tuple[chex.Numeric, nn.State]:
  """Train step in pure jax."""

  model, optimizer = nn.merge(graphdef, state, copy=True)

  def loss_fn(model):
    y_pred = model(x)
    return optax.hinge_loss(y_pred, y).mean()

  loss, grads = nn.value_and_grad(loss_fn)(model)
  optimizer.update(model, grads)
  state = nn.state((model, optimizer))
  return loss, state

