
def rnn_bwd_abstract_eval(dy_aval, dhn_aval, dcn_aval, x_aval, h0_aval, c0_aval,
                          w_aval, y_aval, reserve_space_aval,
                          seq_lengths_aval, input_size: int, hidden_size: int,
                          num_layers: int, dropout: float, bidirectional: bool,
                          cudnn_allow_tf32: bool):
  return x_aval, h0_aval, c0_aval, w_aval

