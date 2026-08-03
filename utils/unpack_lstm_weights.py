import math


def unpack_lstm_weights(
    weights: Array, input_size: int, hidden_size: int, num_layers: int,
    bidirectional: bool
) -> tuple[dict[int, Array], dict[int, Array], dict[int, Array], dict[int,
                                                                      Array]]:
  """Unpack cudnn LSTM weights into individual weights.

  CUDNN LSTM weight layout: (num_layers, num_directions, W_ih, W_hh, b_ih, b_hh)
  Returns W_ih, W_hh, b_ih, b_hh. e.g. W_ih[2][1] is the concat weights of
  4 weights (W_ii, W_if, W_ig, W_io), each of shape (hidden_size, input_size)
  at 2nd layer for the reverse direction. See notations from
  https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html#torch.nn.LSTM.
  """
  flat_shapes = _get_params_shapes_in_lstm(input_size, hidden_size, num_layers,
                                           bidirectional)
  flat_shapes_offset = 0
  w_offsets = 0
  num_directions = 2 if bidirectional else 1
  num_pseudo_layers = num_layers * num_directions

  W_ih: dict[int, Array] = {}
  W_hh: dict[int, Array] = {}
  for l in range(num_pseudo_layers):
    for w_kind in [W_ih, W_hh]:
      shape = flat_shapes[flat_shapes_offset]
      flat_shapes_offset += 1
      num_elems = math.prod(shape)
      w_kind[l] = weights[w_offsets:w_offsets + num_elems].reshape(shape)
      w_offsets += num_elems

  b_ih: dict[int, Array] = {}
  b_hh: dict[int, Array] = {}
  for l in range(num_pseudo_layers):
    for w_kind in [b_ih, b_hh]:
      shape = flat_shapes[flat_shapes_offset]
      flat_shapes_offset += 1
      num_elems = math.prod(shape)
      w_kind[l] = weights[w_offsets:w_offsets + num_elems].reshape(shape)
      w_offsets += num_elems
  return W_ih, W_hh, b_ih, b_hh

