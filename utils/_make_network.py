from typing import List

def _make_network(lstm_hidden_sizes: List[int],
                  mlp_hidden_sizes: List[int],
                  output_dim: int) -> hk.RNNCore:
  """set up the network."""

  layers = []
  for k, hidden_size in enumerate(lstm_hidden_sizes):
    layers += [hk.LSTM(hidden_size, name=f'lstm_layer_{k}'), jax.nn.relu]
  layers += [hk.nets.MLP(mlp_hidden_sizes + [output_dim], name='mlp')]
  return RNNModel(layers)

