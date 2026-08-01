
def init_lstm_weight(rng: PRNGKeyArray, input_size: int, hidden_size: int,
                     num_layers: int, bidirectional: bool):
  """Random initialize LSTM weights from U(-k, k), k=sqrt(1/hidden_size)."""
  param_count = get_num_params_in_lstm(input_size, hidden_size, num_layers,
                                       bidirectional)
  k = np.sqrt(1.0 / hidden_size)
  return jax.random.uniform(
      rng, shape=(param_count,), dtype=jnp.float32, minval=-k, maxval=k)

