
def compute_weight_mat(input_size: core.DimSize,
                       output_size: core.DimSize,
                       scale,
                       translation,
                       kernel: Callable,
                       antialias: bool,
                       edge_padding: bool,
                       radius: int | None):
  dtype = dtypes.result_type(scale, translation)
  inv_scale = 1. / scale
  # When downsampling the kernel should be scaled since we want to low pass
  # filter and interpolate, but when upsampling it should not be since we only
  # want to interpolate.
  kernel_scale = jnp.maximum(inv_scale, 1.) if antialias else 1.

  # sample_f has shape [output_size] and is the floating-point index in the
  # input image corresponding to the center of each output pixel.
  sample_f = ((jnp.arange(output_size, dtype=dtype) + 0.5) * inv_scale -
              translation * inv_scale - 0.5)

  # Evaluate the kernel for all input/output coordinate pairs. If edge_padding
  # is true, this includes k pixels outside the original image.
  if edge_padding:
    assert radius is not None
    if antialias:
      # This case isn't actually reachable from the public APIs at the time of
      # writing, but we did figure it out, so we may as well leave the code.
      concrete_scale = core.concrete_or_error(
          None, scale,
          context="Antialiasing with edge padding requires a static scale."
      )
      inv_scale_val = 1.0 / float(concrete_scale)
      kernel_scale_val = max(inv_scale_val, 1.0)
      k = math.ceil(radius * kernel_scale_val)
    else:
      k = radius
  else:
    k = 0

  expanded_indices = jnp.arange(-k, input_size + k, dtype=dtype)
  if kernel is _area_kernel:
    # Compute the left and right boundaries of each output pixel projected
    # back into the input coordinate system.
    L_i = jnp.arange(output_size, dtype=dtype) * inv_scale - translation * inv_scale
    R_i = L_i + inv_scale

    # Compute the left and right boundaries of each input pixel.
    L_j = jnp.arange(input_size, dtype=dtype)
    R_j = L_j + 1.0

    # The weight is the length of the overlap between the projected output
    # pixel interval [L_i, R_i] and the input pixel interval [L_j, R_j].
    # The overlap of [A, B] and [C, D] is max(0, min(B, D) - max(A, C)).
    weights = jnp.maximum(
        0.0,
        jnp.minimum(R_i[np.newaxis, :], R_j[:, np.newaxis])
        - jnp.maximum(L_i[np.newaxis, :], L_j[:, np.newaxis]),
    )
  else:
    x = jnp.abs(sample_f[np.newaxis, :] - expanded_indices[:, np.newaxis])
    x = x / kernel_scale
    weights = kernel(x)

  if edge_padding:
    # Some of the weights are for indices outside the input image. We use a
    # scatter-add to move their mass onto the relevant edge pixels.
    clamped_indices = jnp.clip(
      expanded_indices.astype(jnp.int32), 0, input_size - 1)
    output_indices = jnp.arange(output_size)
    weight_mat = jnp.zeros((input_size, output_size), dtype=dtype)
    output_indices_expanded = lax.broadcast_in_dim(
        output_indices, (expanded_indices.shape[0], output_size), (1,))
    weight_mat = weight_mat.at[
        clamped_indices[:, np.newaxis], output_indices_expanded
    ].add(weights)
    # Normalize the weights
    total_weight_sum = jnp.sum(weight_mat, axis=0, keepdims=True)
    weights = jnp.where(
        jnp.abs(total_weight_sum) > 1000. * float(np.finfo(np.float32).eps),
        jnp.divide(weight_mat,
                   jnp.where(total_weight_sum != 0, total_weight_sum, 1)),
        0)
  else:
    # Normalize the weights to account for the fact that some or all of the
    # input coordinates might not be in the valid part of the input image.
    total_weight_sum = jnp.sum(weights, axis=0, keepdims=True)
    weights = jnp.where(
        jnp.abs(total_weight_sum) > 1000. * float(np.finfo(np.float32).eps),
        jnp.divide(weights,
                   jnp.where(total_weight_sum != 0, total_weight_sum, 1)),
        0)

    # Zero out weights where the sample location is completely outside the input
    # range. sample_f has already had the 0.5 removed, hence the weird range
    # below.
    input_size_minus_0_5 = core.dimension_as_value(input_size) - 0.5
    weights = jnp.where(
        jnp.logical_and(sample_f >= -0.5,
                        sample_f <= input_size_minus_0_5)[np.newaxis, :],
        weights, 0)

  return weights

