
def net_fn(x):
  """Haiku module for our network."""
  net = hk.Sequential([
      hk.Linear(1024),
      jax.nn.relu,
      hk.Linear(1024),
      jax.nn.relu,
      hk.Linear(1024),
      jax.nn.relu,
      hk.Linear(1024),
      jax.nn.relu,
      hk.Linear(NUM_ACTIONS),
      jax.nn.log_softmax,
  ])
  return net(x)


def net_fn(x):
  """Haiku module for our network."""
  net = hk.Sequential([
      hk.Linear(1024),
      jax.nn.relu,
      hk.Linear(1024),
      jax.nn.relu,
      hk.Linear(1024),
      jax.nn.relu,
      hk.Linear(1024),
      jax.nn.relu,
      hk.Linear(NUM_ACTIONS),
      jax.nn.log_softmax,
  ])
  return net(x)


def net_fn(x):
  """Haiku module for our network."""
  layers = []
  for layer_size in FLAGS.hidden_layer_sizes:
    layers.append(hk.Linear(int(layer_size)))
    layers.append(jax.nn.relu)
  layers.append(hk.Linear(NUM_ACTIONS))
  layers.append(jax.nn.log_softmax)
  net = hk.Sequential(layers)
  return net(x)

