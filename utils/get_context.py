
def get_context(
    mat1: Tensor,
    mat2: Tensor,
    mat1_pre_padded: bool,
    mat2_pre_padded: bool,
    m_padded_length: int,
    k_padded_length: int,
    n_padded_length: int,
) -> AHContext:
    context = AHContext()

    context.add_feature("m", mat1.shape[0])
    context.add_feature("k", mat1.shape[1])
    context.add_feature("n", mat2.shape[1])

    context_add_strides(context, "mat1", mat1.stride())
    context_add_strides(context, "mat2", mat2.stride())

    context.add_feature("m_padded_length", m_padded_length)
    context.add_feature("k_padded_length", k_padded_length)
    context.add_feature("n_padded_length", n_padded_length)

    context.add_feature("mat1_align_size", get_alignment_size(mat1))
    context.add_feature("mat2_align_size", get_alignment_size(mat2))

    context.add_feature("mat1_dtype", mat1.dtype, is_categorical=True)
    context.add_feature("mat2_dtype", mat2.dtype, is_categorical=True)

    context.add_feature("prepadded_mat1", mat1_pre_padded, is_categorical=True)
    context.add_feature("prepadded_mat2", mat2_pre_padded, is_categorical=True)

    context_add_using_tf32(context, mat1.dtype)
    return context


def get_context(default: Context | None = None) -> Context:
  """Returns the currently active `Context`, or a default if no context is active.

  If called within a `with ocp.Context(...)` block, this function returns the
  `Context` object associated with that block (the active context).

  If called outside of any `with` block, this function returns `default`
  if it is provided. If `default` is not provided or `None`, it returns a
  new `Context` instance initialized with default options.

  Note: If a context is active, the `default` parameter is ignored, and the
  active context is always returned. To ensure that an explicitly provided
  context takes precedence over any active context, use the pattern:
  `ctx = explicit_context if explicit_context is not None else get_context()`.

  Args:
    default: A `Context` object to return if no context is active.

  Returns:
    The active `Context` or a default `Context`.
  """
  default = default or Context()
  return _CONTEXT.get(default)

