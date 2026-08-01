
def lstm_ref(x: Array, h_0: Array, c_0: Array, W_ih: dict[int, Array],
             W_hh: dict[int, Array], b_ih: dict[int, Array],
             b_hh: dict[int, Array], seq_lengths: Array, input_size: int,
             hidden_size: int, num_layers: int, dropout: float,
             bidirectional: bool) -> tuple[Array, Array, Array]:
  """Reference implementation of LSTM.

  See https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html#lstm
  https://docs.nvidia.com/deeplearning/cudnn/api/index.html#cudnnRNNMode_t
  """
  if seq_lengths.dtype != jnp.dtype("int32"):
    raise NotImplementedError("`seq_lengths` can only be int32.")
  if dropout != 0.0:
    raise NotImplementedError(
        'Dropout not supported in LSTM reference because we cannot determine CUDNN dropout mask.'
    )

  # TODO(zhangqiaorjc): Handle ragged seq_lengths.
  # batch_size, max_seq_length = x.shape[0], x.shape[1]
  # assert seq_lengths.shape == (batch_size,)
  # for i in range(batch_size):
  #   if int(seq_lengths[i]) != max_seq_length:
  #     raise NotImplementedError('Does not yet support ragged sequences.')

  def lstm_cell(carry, x, *, W_ih, W_hh, b_ih, b_hh):
    h, c = carry
    W_ii, W_if, W_ig, W_io = jnp.split(W_ih, 4, axis=0)
    W_hi, W_hf, W_hg, W_ho = jnp.split(W_hh, 4, axis=0)
    b_ii, b_if, b_ig, b_io = jnp.split(b_ih, 4, axis=0)
    b_hi, b_hf, b_hg, b_ho = jnp.split(b_hh, 4, axis=0)
    i = sigmoid(x @ W_ii.T + b_ii[None] + h @ W_hi.T + b_hi[None])
    f = sigmoid(x @ W_if.T + b_if[None] + h @ W_hf.T + b_hf[None])
    g = tanh(x @ W_ig.T + b_ig[None] + h @ W_hg.T + b_hg[None])
    o = sigmoid(x @ W_io.T + b_io[None] + h @ W_ho.T + b_ho[None])
    c = f * c + i * g
    h = o * tanh(c)
    return (h, c), h

  # here we also output the carry so that we can later slice
  # the correct carry according to seq_lengths, while this takes more memory
  # it is faster than using 'jnp.where' inside the scan loop
  def scan_fn(cell, carry, x):
    carry, y = cell(carry, x)
    return carry, (carry, y)

  seq_first_y = x.transpose(1, 0, 2)
  if not bidirectional:
    final_h = []
    final_c = []
    for l in range(num_layers):
      cell = partial(
          lstm_cell, W_ih=W_ih[l], W_hh=W_hh[l], b_ih=b_ih[l], b_hh=b_hh[l])
      cell_fn = partial(scan_fn, cell)
      out = jax.lax.scan(cell_fn, (h_0[l], c_0[l]),
                                             seq_first_y)
      (h_t, c_t), seq_first_y = _extract_output(seq_lengths, out)
      final_h.append(h_t)
      final_c.append(c_t)
    h_n = jnp.stack(final_h)
    c_n = jnp.stack(final_c)
    return seq_first_y.transpose(1, 0, 2), h_n, c_n

  # bidirectional
  final_h = []
  final_c = []
  seq_first_y_fwd: Array | None = None
  for l in range(num_layers * 2):
    cell = partial(
        lstm_cell, W_ih=W_ih[l], W_hh=W_hh[l], b_ih=b_ih[l], b_hh=b_hh[l])
    cell_fn = partial(scan_fn, cell)
    if l % 2 == 0:
      out = jax.lax.scan(cell_fn, (h_0[l], c_0[l]),
                                                 seq_first_y)
      (h_t, c_t), seq_first_y_fwd = _extract_output(seq_lengths, out)
    else:
      # reverse sequence while keeping padding at the end
      seq_first_y_reversed = _flip_sequence(seq_first_y, seq_lengths)
      out = jax.lax.scan(
          cell_fn, (h_0[l], c_0[l]), seq_first_y_reversed)
      (h_t, c_t), seq_first_y_bwd = _extract_output(seq_lengths, out)
      # align reversed sequence with original sequence
      seq_first_y_bwd = _flip_sequence(seq_first_y_bwd, seq_lengths)
      # Inputs to next layer are concat'ed from fwd and bwd.
      assert seq_first_y_fwd is not None
      seq_first_y = jnp.concatenate([seq_first_y_fwd, seq_first_y_bwd], axis=-1)
    final_h.append(h_t)
    final_c.append(c_t)
  h_n = jnp.stack(final_h)
  c_n = jnp.stack(final_c)
  return seq_first_y.transpose(1, 0, 2), h_n, c_n

