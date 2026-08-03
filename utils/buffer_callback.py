from typing import Callable

def buffer_callback(
    callback: Callable[..., None],
    result_shape_dtypes: object,
    *,
    has_side_effect: bool = False,
    vmap_method: str | None = None,
    input_output_aliases: dict[int, int] | None = None,
    command_buffer_compatible: bool = False,
):
  """An experimental callback that operates in place on device buffers.

  Only supported on CPU and GPU backends.

  Note that the plan is for this to eventually be replaced by a consolidated
  callback API built using JAX mutable arrays, but for now this provides a
  mechanism for prototyping computational kernels using other Python libraries
  including Numpy, PyTorch, Cupy, and others.

  Let's start with a simple example:

    >>> def py_add_one_inplace(ctx, out, x):
    ...   np.asarray(out)[...] = np.asarray(x) + 1
    ...
    >>> x = jnp.array(41, dtype=jnp.int32)
    >>> out_type = jax.ShapeDtypeStruct.like(x)
    >>> add_one = buffer_callback(py_add_one_inplace, out_type)
    >>> add_one(x)  # doctest: +SKIP
    Array(42, dtype=int32)

  In this example, we're executing a numpy computation via JAX, and this could
  have been implemented using :func:`jax.pure_callback`, but in this case, the
  output is being populated in-place. This means that JAX doesn't need to copy
  the output arrays upon returning from the callback. Note that even though the
  callback function operates on mutable buffers, JAX still sees this as an
  operation that consumes and produces regular immutable JAX arrays.

  Unlike the other JAX callback APIs, ``buffer_callback`` requires that the
  user-defined Python function have the following signature:

  .. code-block:: python

    def callback(ctx: ExecutionContext, out, *args) -> None:
      ...

  where ``ctx`` is an instance of
  :class:`~jax.experimental.buffer_callback.ExecutionContext`, which mainly
  provides access to XLA's computation stream when running on GPU, ``out`` is a
  pytree of mutable :class:`~jax.experimental.buffer_callback.Buffer` objects,
  and the ``args`` arguments have the same pytree structure as the inputs, but
  each leaf is :class:`~jax.experimental.buffer_callback.Buffer`. This callback
  should not return any values, and it should overwrite the ``out`` buffers in
  place to output values back to JAX.

  It's important to note that this Python function can't really be called
  except via ```buffer_callback`` itself, because it's not (yet!) possible to
  construct mutable JAX buffers directly in Python.

  The bespoke :class:`~jax.experimental.buffer_callback.Buffer` type is an
  array-like object that supports the ``__array__`` protocol on CPU, the
  ``__cuda_array_interface__`` protocol on GPU, and the ``__dlpack__`` protocol
  on both CPU and GPU.

  Args:
    callback: A Python function with the signature and behavior described above.
    result_shape_dtypes: A pytree whose leaves have ``shape`` and ``dtype``
      attributes, with a structure that matches the expected output of the
      callback function at runtime. :class:`jax.ShapeDtypeStruct` is often used
      to define leaf values.
    has_side_effect: Whether the callback has side effects.
    vmap_method: A string specifying how the callback transforms under
      :func:`~jax.vmap` as described in the docs for :func:`~jax.pure_callback`.
    input_output_aliases: a dictionary mapping the index of some inputs to
      the index of the output that aliases them. These indices are in the
      flattened inputs and outputs.
    command_buffer_compatible: if ``True``, the callback will be traced into
      the command buffer. This means that the Python code should only be
      executed once, and then the operations will be replayed for every
      subsequent call.

  Returns:
    A new callable that accepts :class:`jax.Array` inputs (and pytrees thereof),
    and  pytree of :class:`jax.Array` objects whose structure matches that
    of ``result_shape_dtypes``.

  See Also:
    - :func:`jax.pure_callback`: callback designed for pure host functions.
    - :func:`jax.experimental.io_callback`: callback designed for impure host
      functions.
    - :func:`jax.debug.callback`: callback designed for general-purpose
      debugging.
    - :func:`jax.debug.print`: callback designed for printing.
  """
  flat_shape_dtypes, out_tree = tree_util.tree_flatten(result_shape_dtypes)
  flat_result_avals = tuple(
      core.ShapedArray(x.shape, x.dtype) for x in flat_shape_dtypes
  )

  def wrapped_callback(*args, **kwargs):
    flat_args, in_tree = tree_util.tree_flatten((args, kwargs))

    in_avals = [core.typeof(x) for x in flat_args]
    static_input_output_aliases: list[tuple[int, int]] = []
    if input_output_aliases is not None:
      for i_idx, o_idx in sorted(input_output_aliases.items()):
        i_idx, o_idx = int(i_idx), int(o_idx)
        if i_idx >= len(args):
          raise ValueError(
              f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' "
              f"with input index {i_idx} outside the range [0, "
              f"{len(args)}).")
        if o_idx >= len(flat_result_avals):
          raise ValueError(
              f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' "
              f"with output index {o_idx} outside the range [0, "
              f"{len(flat_result_avals)}).")
        in_aval = in_avals[i_idx]
        out_aval = flat_result_avals[o_idx]
        if not ffi._check_compatible_avals(in_aval, out_aval):
          raise ValueError(
              f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' "
              f"referring to an input with abstract value {in_aval} and an "
              f"output with a different abstract value {out_aval}.")
        static_input_output_aliases.append((i_idx, o_idx))

    out_flat = buffer_callback_p.bind(
        *flat_args,
        callback=callback,
        result_avals=flat_result_avals,
        in_tree=in_tree,
        out_tree=out_tree,
        vmap_method=vmap_method,
        has_side_effect=has_side_effect,
        input_output_aliases=tuple(static_input_output_aliases),
        command_buffer_compatible=command_buffer_compatible,
    )
    return tree_util.tree_unflatten(out_tree, out_flat)

  return wrapped_callback

