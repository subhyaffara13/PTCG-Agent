
def _rnn_forwards(lstm_hidden_sizes: List[int], mlp_hidden_sizes: List[int],
                  batch_size: int) -> hk.Transformed:
  """Returns a haiku transformation of the RNN model to be used in optimizer.

  Args:
    lstm_hidden_sizes: List containing size of lstm layers.
    mlp_hidden_sizes: List containing size of linear layers.
    batch_size: Batch size.

  Returns:
    Haiku transformation of the RNN network.
  """
  def forward_fn(inputs):
    rnn = _make_rnn_network(lstm_hidden_sizes, mlp_hidden_sizes)
    initial_state = rnn.initial_state(batch_size=batch_size)
    outputs, _ = hk.dynamic_unroll(rnn, inputs, initial_state, time_major=False)
    return outputs

  return hk.transform(forward_fn)

