
def lstm_fwd(x: Array, h_0: Array, c_0: Array, w: Array, seq_lengths: Array,
             input_size: int, hidden_size: int, num_layers: int, dropout: float,
             bidirectional: bool, precision: lax.PrecisionLike):
  if seq_lengths.dtype != jnp.dtype("int32"):
    raise NotImplementedError("`seq_lengths` can only be int32.")
  cudnn_allow_tf32 = _lstm_cudnn_allow_tf32(precision)
  y, h_n, c_n, reserve_space = rnn_fwd_p.bind(
      x,
      h_0,
      c_0,
      w,
      seq_lengths,
      input_size=input_size,
      hidden_size=hidden_size,
      num_layers=num_layers,
      dropout=dropout,
      bidirectional=bidirectional,
      cudnn_allow_tf32=cudnn_allow_tf32)
  return (y, h_n, c_n), (x, h_0, c_0, w, seq_lengths, y, reserve_space)

