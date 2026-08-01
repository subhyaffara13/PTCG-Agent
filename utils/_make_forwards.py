
def _make_forwards(lstm_hidden_sizes: List[int], mlp_hidden_sizes: List[int],
                   output_dim: int, batch_size: int) -> hk.Transformed:

  """Forward pass."""

  def forward_fn(inputs):
    rnn = _make_network(lstm_hidden_sizes, mlp_hidden_sizes, output_dim)
    initial_state = rnn.initial_state(batch_size=batch_size)
    outputs, _ = hk.dynamic_unroll(rnn, inputs, initial_state, time_major=False)
    return outputs

  network = hk.transform(forward_fn)
  return network

