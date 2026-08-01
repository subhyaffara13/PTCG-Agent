
def flip_sequences(
  inputs: Array,
  seq_lengths: Array | None,
  num_batch_dims: int,
  time_major: bool,
) -> Array:
  """Flips a sequence of inputs along the time axis.

  This function can be used to prepare inputs for the reverse direction of a
  bidirectional LSTM. It solves the issue that, when naively flipping multiple
  padded sequences stored in a matrix, the first elements would be padding
  values for those sequences that were padded. This function keeps the padding
  at the end, while flipping the rest of the elements.

  Example:
  ```python
  inputs = [[1, 0, 0],
            [2, 3, 0]
            [4, 5, 6]]
  lengths = [1, 2, 3]
  flip_sequences(inputs, lengths) = [[1, 0, 0],
                                     [3, 2, 0],
                                     [6, 5, 4]]
  ```

  Args:
    inputs: An array of input IDs <int>[batch_size, seq_length].
    lengths: The length of each sequence <int>[batch_size].

  Returns:
    An ndarray with the flipped inputs.
  """
  # Compute the indices to put the inputs in flipped order as per above example.
  time_axis = 0 if time_major else num_batch_dims
  max_steps = inputs.shape[time_axis]

  if seq_lengths is None:
    # reverse inputs and return
    inputs = jnp.flip(inputs, axis=time_axis)
    return inputs

  seq_lengths = jnp.expand_dims(seq_lengths, axis=time_axis)

  # create indexes
  idxs = jnp.arange(max_steps - 1, -1, -1)  # [max_steps]
  if time_major:
    idxs = jnp.reshape(idxs, [max_steps] + [1] * num_batch_dims)
  else:
    idxs = jnp.reshape(
      idxs, [1] * num_batch_dims + [max_steps]
    )  # [1, ..., max_steps]
  idxs = (idxs + seq_lengths) % max_steps  # [*batch, max_steps]
  idxs = _expand_dims_like(
    idxs, target=inputs
  )  # [*batch, max_steps, *features]
  # Select the inputs in flipped order.
  outputs = jnp.take_along_axis(inputs, idxs, axis=time_axis)

  return outputs


def flip_sequences(
    inputs: Array,
    seq_lengths: Array | None,
    num_batch_dims: int,
    time_major: bool,
) -> Array:
    """Flips a sequence of inputs along the time axis.

    This function can be used to prepare inputs for the reverse direction of a
    bidirectional LSTM. It solves the issue that, when naively flipping multiple
    padded sequences stored in a matrix, the first elements would be padding
    values for those sequences that were padded. This function keeps the padding
    at the end, while flipping the rest of the elements.

    Example::

      >>> from flax.nnx.nn.recurrent import flip_sequences
      >>> from jax import numpy as jnp
      >>> inputs = jnp.array([[1, 0, 0], [2, 3, 0], [4, 5, 6]])
      >>> lengths = jnp.array([1, 2, 3])
      >>> flip_sequences(inputs, lengths, 1, False)
      Array([[1, 0, 0],
             [3, 2, 0],
             [6, 5, 4]], dtype=int32)


    Args:
      inputs: An array of input IDs <int>[batch_size, seq_length].
      lengths: The length of each sequence <int>[batch_size].

    Returns:
      An ndarray with the flipped inputs.
    """
    # Compute the indices to put the inputs in flipped order as per above example.
    time_axis = 0 if time_major else num_batch_dims
    max_steps = inputs.shape[time_axis]

    if seq_lengths is None:
        # reverse inputs and return
        inputs = jnp.flip(inputs, axis=time_axis)
        return inputs

    seq_lengths = jnp.expand_dims(seq_lengths, axis=time_axis)

    # create indexes
    idxs = jnp.arange(max_steps - 1, -1, -1)  # [max_steps]
    if time_major:
        idxs = jnp.reshape(idxs, [max_steps] + [1] * num_batch_dims)
    else:
        idxs = jnp.reshape(
            idxs, [1] * num_batch_dims + [max_steps]
        )  # [1, ..., max_steps]
    idxs = (idxs + seq_lengths) % max_steps  # [*batch, max_steps]
    idxs = _expand_dims_like(idxs, target=inputs)  # [*batch, max_steps, *features]
    # Select the inputs in flipped order.
    outputs = jnp.take_along_axis(inputs, idxs, axis=time_axis)

    return outputs

