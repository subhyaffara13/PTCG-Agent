
def lstm(g: jit_utils.GraphContext, *args):
    if symbolic_helper._is_tensor_list(args[3]):
        return _lstm_packed(g, *args)
    else:
        return _lstm_full(g, *args)


def lstm(x: Array, h_0: Array, c_0: Array, weights: Array, seq_lengths: Array,
         input_size: int, hidden_size: int, num_layers: int, dropout: float,
         bidirectional: bool, precision: lax.PrecisionLike = None) -> tuple[Array, Array, Array]:
  """LSTM via CuDNN or HIPDNN (not-yet-supported).

  Assume batch-first inputs.

  Arguments:
    x: (batch_size, max_seq_length, input_size)
    h_0: (num_directions * num_layers, batch_size, hidden_size)
    c_0: (num_directions * num_layers, batch_size, hidden_size)
    weights: (num_params,) where num_params = get_num_params_in_lstm(...)
    seq_lengths: (batch_size,)
  Returns: (y, h_n, c_n, reserve_space).
    y: (batch_size, max_seq_length, hidden_size * num_directions)
    h_n: (num_directions * num_layers, batch_size, hidden_size)
    c_n: (num_directions * num_layers, batch_size, hidden_size)
  """
  (y, h_n, c_n), _ = lstm_fwd(
      x,
      h_0,
      c_0,
      weights,
      seq_lengths,
      input_size=input_size,
      hidden_size=hidden_size,
      num_layers=num_layers,
      dropout=dropout,
      bidirectional=bidirectional,
      precision=precision)
  return y, h_n, c_n

