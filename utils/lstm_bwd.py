
def lstm_bwd(input_size: int, hidden_size: int, num_layers: int, dropout: float,
             bidirectional: bool, precision: lax.PrecisionLike,
             residuals, gradients):
  cudnn_allow_tf32 = _lstm_cudnn_allow_tf32(precision)
  x, h_0, c_0, w, seq_lengths, y, reserve_space = residuals
  dy, dh_n, dc_n = gradients
  dx, dh_0, dc_0, dw = rnn_bwd_p.bind(
      dy,
      dh_n,
      dc_n,
      x,
      h_0,
      c_0,
      w,
      y,
      reserve_space,
      seq_lengths,
      input_size=input_size,
      hidden_size=hidden_size,
      num_layers=num_layers,
      dropout=dropout,
      bidirectional=bidirectional,
      cudnn_allow_tf32=cudnn_allow_tf32)
  return (dx, dh_0, dc_0, dw, jnp.zeros_like(seq_lengths))

