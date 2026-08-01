
def rnn_abstract_eval(x_aval, h_0_aval, c_0_aval, w_aval, seq_lengths_aval,
                      input_size: int, hidden_size: int, num_layers: int,
                      dropout: float, bidirectional: bool,
                      cudnn_allow_tf32: bool):
  batch_size, max_seq_length = x_aval.shape[0], x_aval.shape[1]
  num_directions = 2 if bidirectional else 1
  output_shape = (batch_size, max_seq_length, num_directions * hidden_size)
  output_aval = core.ShapedArray(output_shape, x_aval.dtype)
  _, reserve_space_size = (
      # pyrefly: ignore[missing-attribute]
      gpu_rnn.compute_rnn_workspace_reserve_space_sizes(
          input_size, hidden_size, num_layers, batch_size, max_seq_length,
          dropout, bidirectional, cudnn_allow_tf32))
  reserve_space_aval = core.ShapedArray((reserve_space_size,), jnp.float32)
  return output_aval, h_0_aval, c_0_aval, reserve_space_aval

