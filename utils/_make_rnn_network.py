from typing import List

def _make_rnn_network(lstm_hidden_sizes: List[int],
                      mlp_hidden_sizes: List[int]) -> hk.RNNCore:
  """Returns the RNN network.

  Args:
    lstm_hidden_sizes: List containing size of lstm layers.
    mlp_hidden_sizes: List containing size of linear layers.

  Returns:
    Returns an instance of RNN model.
  """
  layers = []
  for k, hidden_size in enumerate(lstm_hidden_sizes):
    layers += [hk.LSTM(hidden_size, name=f"lstm_layer_{k}"), jax.nn.relu]
  layers += [hk.nets.MLP(mlp_hidden_sizes, name="mlp")]
  return RNNModel(layers)

