import math


def _overlap_and_add(x: Array, step_size: int) -> Array:
  """Utility function compatible with tf.signal.overlap_and_add.

  Args:
    x: An array with `(..., frames, frame_length)`-shape.
    step_size: An integer denoting overlap offsets. Must be less than
      `frame_length`.

  Returns:
    An array with `(..., output_size)`-shape containing overlapped signal.
  """
  check_arraylike("_overlap_and_add", x)
  step_size = core.concrete_or_error(
      int, step_size, "step_size for overlap_and_add")
  if x.ndim < 2:
    raise ValueError('Input must have (..., frames, frame_length) shape.')

  *batch_shape, nframes, segment_len = x.shape
  flat_batchsize = math.prod(batch_shape)
  x = x.reshape((flat_batchsize, nframes, segment_len))
  output_size = step_size * (nframes - 1) + segment_len
  nstep_per_segment = 1 + (segment_len - 1) // step_size

  # Here, we use shorter notation for axes.
  # B: batch_size, N: nframes, S: nstep_per_segment,
  # T: segment_len divided by S

  padded_segment_len = nstep_per_segment * step_size
  x = jnp.pad(x, ((0, 0), (0, 0), (0, padded_segment_len - segment_len)))
  x = x.reshape((flat_batchsize, nframes, nstep_per_segment, step_size))

  # For obtaining shifted signals, this routine reinterprets flattened array
  # with a shrunken axis.  With appropriate truncation/ padding, this operation
  # pushes the last padded elements of the previous row to the head of the
  # current row.
  # See implementation of `overlap_and_add` in Tensorflow for details.
  x = x.transpose((0, 2, 1, 3))  # x: (B, S, N, T)
  x = jnp.pad(x, ((0, 0), (0, 0), (0, nframes), (0, 0)))  # x: (B, S, N*2, T)
  shrunken = x.shape[2] - 1
  x = x.reshape((flat_batchsize, -1))
  x = x[:, :(nstep_per_segment * shrunken * step_size)]
  x = x.reshape((flat_batchsize, nstep_per_segment, shrunken * step_size))

  # Finally, sum shifted segments, and truncate results to the output_size.
  x = x.sum(axis=1)[:, :output_size]
  return x.reshape(tuple(batch_shape) + (-1,))

