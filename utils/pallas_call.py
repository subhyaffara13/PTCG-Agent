
def pallas_call(
    kernel: Callable[..., None],
    out_shape: Any,
    *,
    grid_spec: pallas_core.GridSpec | None = None,
    grid: pallas_core.TupleGrid = (),
    in_specs: pallas_core.BlockSpecTree = no_block_spec,
    out_specs: pallas_core.BlockSpecTree = no_block_spec,
    scratch_shapes: pallas_core.ScratchShapeTree = (),
    input_output_aliases: Mapping[int, int] = {},
    debug: bool = False,
    interpret: Any = False,
    name: str | None = None,
    compiler_params: pallas_core.CompilerParams | None = None,
    cost_estimate: CostEstimate | None = None,
    metadata: dict[str, str] | None = None,
) -> Callable[..., Any]:
  """Entry point for creating a Pallas kernel.

  In contrast to :func:`jax.experimental.pallas.kernel`, this entry point
  assumes that the kernel will be executed over a ``grid``.

  See `Pallas Quickstart
  <https://docs.jax.dev/en/latest/pallas/quickstart.html>`_.

  Args:
    kernel: the kernel function, that receives a Ref for each input and output.
      The shape of the Refs are given by the ``block_shape`` in the
      corresponding ``in_specs`` and ``out_specs``.
    out_shape: a PyTree of :class:`jax.ShapeDtypeStruct` describing the shape
      and dtypes of the outputs.
    grid_spec: An alternative way to specify ``grid``, ``in_specs``,
      ``out_specs`` and ``scratch_shapes``. If given, those other parameters
      must not be also given.
    grid: the iteration space, as a tuple of integers. The kernel is executed as
      many times as ``prod(grid)``. See details at :ref:`pallas_grid`.
    in_specs: a PyTree of :class:`jax.experimental.pallas.BlockSpec` with a
      structure matching that of the positional arguments. The default value for
      ``in_specs`` specifies the whole array for all inputs, e.g., as
      ``pl.BlockSpec(x.shape, lambda *indices: (0,) * x.ndim)``. See details at
      :ref:`pallas_blockspec`.
    out_specs: a PyTree of :class:`jax.experimental.pallas.BlockSpec` with a
      structure matching that of the outputs. The default value for
      ``out_specs`` specifies the whole array, e.g., as ``pl.BlockSpec(x.shape,
      lambda *indices: (0,) * x.ndim)``. See details at :ref:`pallas_blockspec`.
    scratch_shapes: a PyTree of backend-specific temporary objects required by
      the kernel, such as temporary buffers, synchronization primitives, etc.
    input_output_aliases: a dictionary mapping the index of some inputs to the
      index of the output that aliases them. These indices are in the flattened
      inputs and outputs (ignoring None values).
    debug: if True, Pallas prints various intermediate forms of the kernel as it
      is being processed.
    interpret: runs the ``pallas_call`` as a ``jax.jit`` of a scan over the grid
      whose body is the kernel lowered as a JAX function. This does not require
      a TPU or a GPU, and is the only way to run Pallas kernels on CPU. This is
      useful for debugging.
    name: if present, specifies the name to use for this kernel call in
      debugging and error messages. To this name we append the file and line
      where the kernel function is defined, .e.g: `{name} for kernel function
      {kernel_name} at {file}:{line}`. If missing, then we use `{kernel_name} at
      {file}:{line}`.
    compiler_params: Optional compiler parameters. The value should be a
      backend-specific dataclass
      (:class:`jax.experimental.pallas.tpu.CompilerParams`,
      :class:`jax.experimental.pallas.triton.CompilerParams`,
      :class:`jax.experimental.pallas.mosaic_gpu.CompilerParams`).
    metadata: Optional dictionary of information about the kernel that will be
      serialized as JSON in the HLO. Can be used for debugging and analysis.

  Returns:
    A function that can be called on a number of positional array arguments to
    invoke the Pallas kernel.
  """
  flat_scratch_shapes, scratch_tree = tree_util.tree_flatten(scratch_shapes)
  if grid_spec is None:
    grid_spec = pallas_core.GridSpec(grid, in_specs, out_specs, flat_scratch_shapes)
  else:
    if grid:
      raise ValueError(
          "If `grid_spec` is specified, then `grid` must "
          f"be `()`. It is {grid}")
    if in_specs is not no_block_spec:
      raise ValueError(
          "If `grid_spec` is specified, then `in_specs` must "
          f"be `no_block_spec`. It is {in_specs}")
    if out_specs is not no_block_spec:
      raise ValueError(
          "If `grid_spec` is specified, then `out_specs` must "
          f"be `no_block_spec`. It is {out_specs}")
    if scratch_shapes:
      raise ValueError(
          "If `grid_spec` is specified, then `scratch_shapes` must "
          f"be `()`. It is {scratch_shapes}")
  del grid, in_specs, out_specs
  return _pallas_call(
      kernel,
      out_shape,
      grid_spec=grid_spec,
      scratch_tree=scratch_tree,
      input_output_aliases=input_output_aliases,
      debug=debug,
      interpret=interpret,
      name=name,
      compiler_params=compiler_params,
      cost_estimate=cost_estimate,
      metadata=metadata,
  )

