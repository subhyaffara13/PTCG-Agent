
def kernel(
    body: Callable | Sequence[Callable] | api.NotSpecified = api.NotSpecified(),
    out_type: object = (),
    *,
    mesh: pl_core.Mesh | Sequence[pl_core.Mesh],
    scratch_types: pl_core.ScratchShapeTree = (),
    compiler_params: pl_core.CompilerParams | None = None,
    interpret: Any = False,
    cost_estimate: pl_core.CostEstimate | None = None,
    debug: bool = False,
    name: str | None = None,
    metadata: dict[str, str] | None = None,
):
  r"""Entry point for creating a Pallas kernel.

  This is a convenience wrapper around ``mpmd_map`` for executing a kernel
  over a mesh.

  If ``body`` is provided, this function behaves as a decorator:

  .. code-block:: python

    def kernel_body(in_ref, out_ref):
      ...
    kernel = pl.kernel(kernel_body, out_type=...)

  If ``body`` is omitted, this function behaves as a decorator factory and
  will return a decorator that can be used to annotate a kernel body:

  .. code-block:: python

    @pl.kernel(mesh=..., out_type=...)
    def kernel(in_ref, out_ref):
      ...

  For MPMD kernels, you can pass parallel lists of bodies and meshes:

  .. code-block:: python

    my_kernel = pl.kernel(
        body=[vector_fn, scalar_fn],
        mesh=[v_mesh, s_mesh],
        out_type=...
    )

  JAX ``Ref`` objects can be closed over by the kernel body or passed in as
  arguments. Any such ``Ref`` will be treated as if it is read-from and
  written-to and will be aliased in and out of the kernel.

  .. code-block:: python

    @pl.kernel(mesh=...)
    def kernel(in_ref, out_ref):
      ...
    x_ref = jax.new_ref(...)
    y_ref = jax.new_ref(...)
    kernel(x_ref, y_ref)  # Can now mutate x_ref and y_ref

  Args:
    body: The body of the kernel. If provided, this function behaves as a
      decorator, and if omitted, this function behaves as a decorator factory.
      Can also be a sequence of callables to be paired with a sequence of
      meshes.
    out_type: The type of the output. Should be a PyTree of
      ``jax.ShapeDtypeStruct`` or JAX types.
    mesh: The mesh to run the kernel on. Must be a sequence of meshes if
      ``body`` is a sequence of callables.
    scratch_types: The types of the scratch ``Ref``\s to allocate. Should be a
      PyTree of ``jax.ShapeDtypeStruct`` or JAX types.
    compiler_params: The compiler parameters to pass to the backend.
    interpret: Whether to run the function in interpret mode.
    debug: Whether or not to out helpful debugging information.
    cost_estimate: The cost estimate of the function.
    name: The (optional) name of the kernel.
    metadata: Optional dictionary of information about the kernel that will be
      serialized as JSON in the HLO. Can be used for debugging and analysis.

  Returns:
    If ``body`` is provided, returns a function that runs the kernel.
    It should take any number of input operands and returns an output with the
    same PyTree structure as `out_type`.
    If ``body`` is omitted, returns a decorator that can be used to annotate
    a kernel body.
  """
  # Note we default out_shape to None to allow `body` to come before it
  # in the function signature, but `body` itself is optional.
  make_kernel = functools.partial(
      mpmd.mpmd_map,
      out_types=out_type,
      scratch_types=scratch_types,
      compiler_params=compiler_params,
      interpret=(
          config.pallas_tpu_interpret_mode_context_manager.value or interpret
      ),
      cost_estimate=cost_estimate,
      debug=debug,
      name=name,
      metadata=metadata,
  )

  if isinstance(body, api.NotSpecified):
    # Decorator mode.
    if isinstance(mesh, Sequence):
      raise ValueError(
          "mesh cannot be a sequence when using pl.kernel as a decorator."
      )
    return lambda fun: make_kernel([(mesh, fun)])
  elif isinstance(body, Sequence):
    # MPMD mode.
    if not isinstance(mesh, Sequence):
      raise ValueError(
          "mesh must be a sequence when body is a sequence of callables."
      )
    if len(body) != len(mesh):
      raise ValueError("body and mesh sequences must have the same length.")
    meshes_and_fns = list(zip(mesh, body))
    return make_kernel(meshes_and_fns)
  # Single kernel.
  if isinstance(mesh, Sequence):
    raise ValueError(
        "mesh cannot be a sequence when body is a single callable."
    )
  return make_kernel([(mesh, body)])


def kernel(
    body: Callable[..., None] | api.NotSpecified = api.NotSpecified(),
    out_shape: object | api.NotSpecified = api.NotSpecified(),
    *,
    out_type: object | api.NotSpecified = api.NotSpecified(),
    scratch_types: ScratchShapeTree | api.NotSpecified = api.NotSpecified(),
    scratch_shapes: ScratchShapeTree | api.NotSpecified = api.NotSpecified(),
    compiler_params: pallas_core.CompilerParams | None = None,
    # Mesh kwargs
    grid: tuple[int, ...] = (),
    grid_names: tuple[str, ...] = (),
    cluster: tuple[int, ...] = (),
    cluster_names: tuple[str, ...] = (),
    num_threads: int | None = None,
    thread_name: str | None = None,
    interpret: Any = None,
    **mesh_kwargs: Any,
) -> Any:
  r"""Entry point for defining a Mosaic GPU kernel.

  Args:
    body: The kernel body, which should take as arguments the input, output, and
      scratch Refs. The number of input Refs is determined by the number of
      arguments passed into kernel returned by this function. The number of
      output and scratch Refs are determined by `out_shape` and `scratch_shapes`
      respectively.
    out_shape: A deprecated alias for ``out_type``.
    out_type: The type of the output. Should be a PyTree of
      ``jax.ShapeDtypeStruct`` or JAX types.
    scratch_shapes: A deprecated alias for ``scratch_types``.
    scratch_types: The types of the scratch ``Ref``\s to allocate. Should be a
      PyTree of ``jax.ShapeDtypeStruct`` or JAX types.
    compiler_params: Additional compiler options. See the `CompilerParams`
      dataclass for more details.
    grid: A tuple of integers specifying the size of the kernel grid.
    grid_names: The axis names of the grid. Must be the same length as `grid`.
    cluster: A tuple of integers specifying the size of the kernel cluster.
    cluster_names: The axis names of the grid. Must be the same length as
      `cluster`.
    num_threads: The number of threads to launch per block. Note that these do
      not correspond to CUDA threads, but rather to warpgroups on Hopper and
      Blackwell GPUs.
    thread_name: The axis name used to query the thread index.
    **mesh_kwargs: Additional mesh kwargs. See `Mesh` for more details.

  Returns:
    If ``body`` is provided, returns a function that runs the kernel. It should
    take any number of input operands and returns an output with the same PyTree
    structure as ``out_shape``.

    If ``body`` is omitted, returns a decorator that can be used to annotate
    a kernel body.
  """
  if isinstance(body, api.NotSpecified):
    return lambda fun: kernel(
        fun,
        out_shape,
        out_type=out_type,
        scratch_shapes=scratch_shapes,
        scratch_types=scratch_types,
        compiler_params=compiler_params,
        grid=grid,
        grid_names=grid_names,
        cluster=cluster,
        cluster_names=cluster_names,
        num_threads=num_threads,
        thread_name=thread_name,
        interpret=interpret,
        **mesh_kwargs,
    )

  if (
      not isinstance(out_shape, api.NotSpecified)
      or not isinstance(scratch_shapes, api.NotSpecified)
  ):
    deprecations.warn(
        "jax-pallas-mgpu-shapes-types",
        "The out_shape and scratch_shapes arguments to plgpu.kernel are"
        " deprecated. Use out_type and scratch_types instead.",
        stacklevel=2,
    )

  if not isinstance(out_shape, api.NotSpecified):
    if not isinstance(out_type, api.NotSpecified):
      raise ValueError(
          "Cannot specify both out_shape and out_type. Use out_type."
      )
    out_type = out_shape
  elif isinstance(out_type, api.NotSpecified):
    out_type = ()

  if not isinstance(scratch_shapes, api.NotSpecified):
    if not isinstance(scratch_types, api.NotSpecified):
      raise ValueError(
          "Cannot specify both scratch_shapes and scratch_types. Use"
          " scratch_types."
      )
    scratch_types = scratch_shapes
  elif isinstance(scratch_types, api.NotSpecified):
    scratch_types = ()

  if unwrap_out := not isinstance(out_type, (tuple, list)):
    out_type = (out_type,)

  mesh = Mesh(
      grid=grid,
      grid_names=grid_names,
      cluster=cluster,
      cluster_names=cluster_names,
      num_threads=num_threads,
      thread_name=thread_name,
      **mesh_kwargs,
  )

  # TODO(slebedev): Use mesh-specific batching rules in ``mpmd_map`` instead.
  @custom_batching.custom_vmap
  def wrapper(*operands):
    thread_name = mesh.thread_name if mesh.thread_name is not None else ()

    def kernel_body(*refs):
      # NOTE: We cannot use the ``scratch_types=`` argument of ``pl.kernel``
      # for these, because some scratch types return ``TransformedRef``s in
      # ``get_ref_aval``, which is not yet supported by ``mpmd_map``.
      pallas_primitives.run_scoped(
          functools.partial(body, *refs),
          *scratch_types if isinstance(scratch_types, Sequence) else (),
          collective_axes=thread_name,
          **scratch_types if isinstance(scratch_types, Mapping) else {},
      )

    name = (
        getattr(body, "__name__", "anonymous")
        if mesh.kernel_name is None
        else mesh.kernel_name
    )
    # TODO(slebedev): This is only here for backward compatibility. Remove.
    with config._check_vma(False):
      outs = pallas_helpers.kernel(
          kernel_body,
          out_type=out_type,
          mesh=mesh,
          compiler_params=compiler_params,
          interpret=interpret,
          name=name,
      )(*operands)
    return outs[0] if unwrap_out else outs

  @wrapper.def_vmap
  def _vmap_rule(axis_size, in_batched, *args):
    axis_name = object()

    def batched_body(*refs, **scratch_ref_kwargs):
      idx = lax.axis_index(axis_name)
      lens = (len(args), len(out_type))
      operand_refs, out_refs, scratch_refs = util.split_list(refs, lens)
      slice_ref = lambda r, b=True: (r.at[idx] if b else r)
      operand_refs = tree_util.tree_map(slice_ref, operand_refs, in_batched)
      out_refs = tree_util.tree_map(slice_ref, out_refs)
      return body(*operand_refs, *out_refs, *scratch_refs, **scratch_ref_kwargs)

    out_type_ = out_type[0] if unwrap_out else out_type
    add_batch_dim = lambda x: x.update(shape=(axis_size, *x.shape))
    mesh_kwargs_ = dict(mesh_kwargs)
    out = kernel(
        batched_body,
        out_type=tree_util.tree_map(add_batch_dim, out_type_),
        scratch_types=scratch_types,
        compiler_params=compiler_params,
        grid=(axis_size,) + grid,
        grid_names=(axis_name,) + grid_names,  # pyrefly: ignore[bad-argument-type]
        cluster=cluster,
        cluster_names=cluster_names,
        num_threads=num_threads,
        thread_name=thread_name,
        interpret=interpret,
        **mesh_kwargs_,
    )(*args)
    out_batched = tree_util.tree_map(lambda _: True, out_type_)
    return out, out_batched

  return wrapper


def kernel(a_gmem, b_gmem, c_gmem, out_gmem, config: TuningConfig,
           pipeline_callback=None, delay_release=0):
  dtype = a_gmem.dtype
  out_dtype = out_gmem.dtype
  assert b_gmem.dtype == dtype
  if c_gmem is not None:
    assert c_gmem.dtype == out_dtype
  m, k = a_gmem.shape
  k2, n = b_gmem.shape
  assert k == k2
  tile_m, tile_n, tile_k = config.tile_m, config.tile_n, config.tile_k
  max_concurrent_steps = config.max_concurrent_steps
  swizzle = plgpu.find_swizzle(tile_k * jnp.dtype(dtype).itemsize * 8)
  swizzle_elems = swizzle // jnp.dtype(dtype).itemsize
  transforms = (
      plgpu.TilingTransform((8, swizzle_elems)), plgpu.SwizzleTransform(swizzle)
  )

  cta_tile_m = tile_m * (1 + (config.wg_dimension == MatmulDimension.M))
  cta_tile_n = tile_n * (1 + (config.wg_dimension == MatmulDimension.N))
  cluster_tile_m = cta_tile_m * (1 + (config.cluster_dimension == MatmulDimension.M))
  cluster_tile_n = cta_tile_n * (1 + (config.cluster_dimension == MatmulDimension.N))
  if m % cluster_tile_m != 0:
    raise ValueError(f"{m=} must be divisible by {cluster_tile_m} for the given config")
  if n % cluster_tile_n != 0:
    raise ValueError(f"{n=} must be divisible by {cluster_tile_n} for the given config")
  if k % tile_k != 0:
    raise ValueError(f"{k=} must be divisible by {tile_k=}")
  m_iters = m // cluster_tile_m
  n_iters = n // cluster_tile_n
  k_iters = k // tile_k

  epi_tile_m = config.epi_tile_m or tile_m
  epi_tile_n = config.epi_tile_n or tile_n
  # We don't need multiple slots if there's only one epilogue tile.
  num_out_slots = min(2, (tile_m * tile_n) // (epi_tile_m * epi_tile_n))
  out_swizzle = plgpu.find_swizzle(epi_tile_n * jnp.dtype(out_dtype).itemsize * 8)
  out_swizzle_elems = out_swizzle // jnp.dtype(out_dtype).itemsize
  out_transforms = (
      plgpu.TilingTransform((8, out_swizzle_elems)),
      plgpu.SwizzleTransform(out_swizzle),
  )

  def get_pipeline(pipeline_body, compute_context):
    return plgpu.emit_pipeline_warp_specialized(
        pipeline_body,
        grid=(k_iters,),
        memory_registers=40,
        in_specs=[
            plgpu.BlockSpec(
                (cta_tile_m, tile_k),
                lambda k: (0, k),
                transforms=transforms,
                memory_space=plgpu.SMEM,
                delay_release=delay_release,
                collective_axes=("cluster",)
                if config.cluster_dimension == MatmulDimension.N
                else (),
            ),
            plgpu.BlockSpec(
                (tile_k, cta_tile_n),
                lambda k: (k, 0),
                transforms=transforms,
                memory_space=plgpu.SMEM,
                delay_release=delay_release,
                collective_axes=("cluster",)
                if config.cluster_dimension == MatmulDimension.M
                else (),
            ),
        ],
        wg_axis="wg",
        num_compute_wgs=2,
        max_concurrent_steps=max_concurrent_steps,
        compute_context=compute_context,
    )

  # Functions don't influence the allocations necessary to run the pipeline.
  ignore = lambda *_, **__: None
  @functools.partial(
      pl.run_scoped,
      pipeline_allocs=get_pipeline(ignore, ignore).get_allocations(a_gmem, b_gmem),
      out_smem=plgpu.SMEM(
          (2, num_out_slots, epi_tile_m, epi_tile_n),
          out_dtype,
          transforms=out_transforms,
      ),
      c_barrier=None if c_gmem is None else plgpu.Barrier(num_barriers=2 * num_out_slots),
      collective_axes="wg",
  )
  def _pipeline_scope(pipeline_allocs, out_smem, c_barrier):
    wg_idx = lax.axis_index("wg")
    cta_idx = lax.axis_index("cluster")
    @plgpu.nd_loop((m_iters * n_iters,), collective_axes="cluster_grid")
    def _mn_loop(loop_info: plgpu.NDLoopInfo):
      (lin_idx,) = loop_info.index
      m_cluster_idx, n_cluster_idx = plgpu.planar_snake(
          lin_idx,
          (m_iters, n_iters),
          config.grid_minor_dim,
          config.grid_tile_width,
      )
      m_idx = m_cluster_idx
      n_idx = n_cluster_idx
      if config.cluster_dimension == MatmulDimension.M:
        m_idx = m_cluster_idx * 2 + cta_idx
      elif config.cluster_dimension == MatmulDimension.N:
        n_idx = n_cluster_idx * 2 + cta_idx
      cta_m_slice = pl.ds(m_idx * cta_tile_m, cta_tile_m)
      cta_n_slice = pl.ds(n_idx * cta_tile_n, cta_tile_n)
      if config.wg_dimension == MatmulDimension.M:
        wg_m_slice = pl.ds(wg_idx * tile_m, tile_m)
        wg_n_slice = slice(None)
      else:
        wg_m_slice = slice(None)
        wg_n_slice = pl.ds(wg_idx * tile_n, tile_n)

      def compute_context(eval_pipeline):
        @functools.partial(
            pl.run_scoped, acc_ref=plgpu.ACC((tile_m, tile_n), jnp.float32)
        )
        def _acc_scope(acc_ref):
          eval_pipeline(acc_ref)
          acc = acc_ref[...].astype(out_dtype)
          plgpu.wait_smem_to_gmem(0, wait_read_only=True)
          for epi_mi in range(tile_m // epi_tile_m):
            for epi_ni in range(tile_n // epi_tile_n):
              epi_m_slice = slice(epi_mi * epi_tile_m, (epi_mi + 1) * epi_tile_m)
              epi_n_slice = slice(epi_ni * epi_tile_n, (epi_ni + 1) * epi_tile_n)
              slot = (epi_mi * (tile_n // epi_tile_n) + epi_ni) % 2
              plgpu.wait_smem_to_gmem(1, wait_read_only=True)
              if c_gmem is None:
                out_smem[wg_idx, slot] = acc[epi_m_slice, epi_n_slice]
              else:
                # TODO: Consider using triple-buffering so to not end up issuing
                # the copy and immediately blocking on it
                plgpu.copy_gmem_to_smem(
                    c_gmem.at[cta_m_slice, cta_n_slice]
                    .at[wg_m_slice, wg_n_slice]
                    .at[epi_m_slice, epi_n_slice],
                    out_smem.at[wg_idx, slot],
                    c_barrier.at[wg_idx * num_out_slots + slot],
                )
                plgpu.barrier_wait(c_barrier.at[wg_idx * num_out_slots + slot])
                out_smem[wg_idx, slot] += acc[epi_m_slice, epi_n_slice]
              plgpu.commit_smem()
              plgpu.copy_smem_to_gmem(
                  out_smem.at[wg_idx, slot],
                  out_gmem.at[cta_m_slice, cta_n_slice]
                  .at[wg_m_slice, wg_n_slice]
                  .at[epi_m_slice, epi_n_slice],
              )

      def mma_body(idxs, a_smem, b_smem, acc_ref):
        plgpu.wgmma(acc_ref, a_smem.at[wg_m_slice], b_smem.at[:, wg_n_slice])
        if pipeline_callback is not None:
          (k_idx,) = idxs
          pipeline_callback(m_idx, n_idx, k_idx, a_smem, b_smem)
        plgpu.wgmma_wait(delay_release)
        return acc_ref

      get_pipeline(mma_body, compute_context)(
          a_gmem.at[cta_m_slice, :],
          b_gmem.at[:, cta_n_slice],
          allocations=pipeline_allocs,
      )
  # Await all transfers before we exit.
  plgpu.wait_smem_to_gmem(0, wait_read_only=True)

