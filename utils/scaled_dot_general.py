
def scaled_dot_general(
    lhs, rhs,
    dimension_numbers,
    preferred_element_type=np.float32,
    configs: list[BlockScaleConfig] | None = None,
    implementation: Literal['cudnn'] | None = None,
  ):
  r"""Scaled dot general operation.

  Performs a generalized dot product with block-scaled quantization on the
  lhs and rhs inputs. This operation extends `lax.dot_general` to support
  user-defined scaling configurations.

  Essentially, the operation follows::

      a, a_scales = quantize(lhs, configs[0])
      b, b_scales = quantize(rhs, configs[1])
      c = jax.nn.scaled_matmul(a, b, a_scales, b_scales)

  Args:
    lhs (ArrayLike): Input array.
    rhs (ArrayLike): Input array.
    dimension_numbers (DotDimensionNumbers): A tuple of two tuples specifying
      the contraction and batch dimensions:
      `((lhs_contracting_dims, rhs_contracting_dims), (lhs_batch_dims, rhs_batch_dims))`.
    preferred_element_type (DTypeLike, optional): Output data type of the dot
      product. Defaults to `jnp.float32`. Other valid types include
      `jnp.bfloat16` and `jnp.float16`.
    configs (list of BlockScaleConfig, optional): Scaling configurations for
      lhs, rhs, and gradients. Users can obtain valid configurations via
      `jax.nn.get_scaled_dot_general_config`. Currently, `nvfp4` and `mxfp8`
      are supported. If `None`, falls back to `lax.dot_general`.
    implementation: str
      (Deprecated) Backend selector, now ignored. The system chooses the backend
      automatically. Scheduled for removal in future releases.

  Returns:
    Array: The resulting tensor, with batch dimensions first, followed by
    non-contracting/non-batch dimensions of lhs, and then those of rhs.

  See Also:
    - :func:`jax.nn.scaled_matmul`: Scaled matmul function.
    - :func:`jax.lax.dot_general`: General dot product operator.

  Notes:
    - Unlike `nn.scaled_matmul`, which assumes quantized low-precision
      inputs with explicit scaling factors, this operator takes high-precision
      inputs, applies quantization internally, and handles the backward pass.

  Examples:

    Creating config for mxfp8:

    >>> configs = [jax.nn.get_scaled_dot_general_config('mxfp8')] * 3

    Creating config for nvfp4:

    >>> global_scale = jnp.array([0.5], jnp.float32)
    >>> configs = [jax.nn.get_scaled_dot_general_config('nvfp4', global_scale)] * 3

    Using scaled_dot_general with the configs:

    >>> import functools
    >>> scaled_dot_general_fn = functools.partial(jax.nn.scaled_dot_general, configs=configs)
    >>> lhs = jax.random.normal(jax.random.PRNGKey(1), (3, 128, 64))
    >>> rhs = jax.random.normal(jax.random.PRNGKey(2), (3, 128, 64))
    >>> out = scaled_dot_general_fn(lhs, rhs, (((2,), (2,)), ((0,), (0,))))  # doctest: +SKIP
  """
  if implementation is not None:
    warnings.warn("Backend selector, now ignored. The system chooses the "
                  "backend automatically.", DeprecationWarning)

  if configs is None:
    return lax.dot_general(lhs, rhs, dimension_numbers,
                           preferred_element_type=preferred_element_type)

  out = cudnn_scaled_dot_general(
      lhs, rhs, dimension_numbers,
      preferred_element_type=preferred_element_type,
      configs=configs
  )

  return out

