import functools
from typing import Any
import math


def interpret_pallas_call(
    *args,
    jaxpr: jax_core.Jaxpr,
    debug: bool,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: pallas_core.GridMapping,
    mesh: plgpu.Mesh | None,
    compiler_params: Mapping[str, Any],
    cost_estimate: pallas_core.CostEstimate,
    out_avals: tuple[jax_core.AbstractValue, ...],
    interpret_params: InterpretGPUParams,
    metadata: Mapping[str, str] | None,
    kernel_arg_transforms: tuple[tuple[state_types.Transform, ...], ...] = (),
    **kwargs,
) -> Sequence[Array]:
  # TODO(nrink): A more fleshed out implementation of the GPU interpreter may
  # need to use some of these `del`ed arguments.
  del debug, cost_estimate, metadata, out_avals, kwargs

  # TODO(nrink): Support non-trivial `BlockSpec`s (i.e. with non-trivial
  # `index_map`s).
  assert all(bm.has_trivial_window() for bm in grid_mapping.block_mappings)

  grid_dims, cluster_dims, num_threads = (
      _get_grid_and_cluster_dims_and_num_threads(grid_mapping, mesh)
  )
  num_blocks_per_cluster = math.prod(cluster_dims)
  device_info = jaxpr_interpret.DeviceInfo()

  interpret_params = dataclasses.replace(
      interpret_params, num_cores_or_threads=num_threads
  )

  # We pass our `token` through an ordered IO callback at the start and end of
  # the interpreted kernel, to ensure that execution of this interpreted kernel
  # cannot overlap with the interpretation of any other kernel.
  token = jnp.int32(42)
  token = callback.io_callback(
      gpu_callbacks.ordering_barrier,
      gpu_callbacks.TOKEN_SHAPE_DTYPE,
      token,
      ordered=True,
  )

  token = gpu_callbacks.call_initialize_shared_memory(
      token=token,
      num_gpus=jnp.int32(device_info.num_devices),
      num_threads_per_block=jnp.int32(num_threads),
      num_blocks_per_cluster=jnp.int32(num_blocks_per_cluster),
      interpret_params=interpret_params,
  )

  dynamic_grid_args, scalars, inputs = split_list(
      args,
      [grid_mapping.num_dynamic_grid_bounds, grid_mapping.num_index_operands],
  )
  if dynamic_grid_args:
    raise NotImplementedError("Dynamic grid bounds not (yet) supported on GPU")
  if scalars:
    raise NotImplementedError("Scalar arguments not (yet) supported on GPU")

  assert grid_mapping.num_index_operands == 0

  token, input_buffer_keys = _allocate_buffers_for_inputs(
      token,
      device_info.device_id,
      jaxpr.invars[: grid_mapping.num_inputs],
      inputs,
  )

  token, output_buffers = _allocate_buffers_for_outputs(
      token,
      device_info.device_id,
      num_threads,
      input_output_aliases,
      grid_mapping,
      input_buffer_keys,
      inputs,
      interpret_params,
  )

  token, kernel_buffer_keys = _get_kernel_buffers(
      token,
      device_info.device_id,
      num_threads,
      grid_mapping,
      jaxpr.invars,
      kernel_arg_transforms,
      input_buffer_keys,
      [buffer.key for buffer in output_buffers],
      interpret_params,
  )

  # TODO(nrink): The two assignments below have been taken from the
  # corresponding TPU interpreter code. Confirm that they make sense here (i.e.
  # for GPU kernels).
  kernel_input_buffer_keys, kernel_output_buffer_keys, _ = split_list(
      kernel_buffer_keys, [grid_mapping.num_inputs, grid_mapping.num_outputs]
  )
  input_vars, output_vars = split_list(
      jaxpr.invars[grid_mapping.slice_block_ops], [grid_mapping.num_inputs]
  )

  def _kernel(thread_id, token, grid_point_coords):
    # Note that the copying from `GMEM` buffers here could introduce races when
    # multiple threads copy to the same kernel input buffer. For this to happen,
    # (a) there must be multiple threads and (b) the targeted kernel input
    # buffer must not be in `GMEM` (since we omit copies from `GMEM` to `GMEM`).
    # Currently, the ways in which a Pallas GPU kernel can be invoked do not
    # allow for (a) and (b) to be true at the same time: (a) requires that the
    # kernel is *not* invoked through a `pallas_call` but (b) can only be caused
    # if `BlockSpec`s are used when invoking the kernels, which requires that
    # the kernel be invoked through a `pallas_call`.
    #
    # TODO(nrink): Support copying of slices/blocks only, based on the
    # `BlockSpec`s. (Currently only trivial `BlockSpec`s are supported.)
    token = _copy_from_gmem_buffers(
        token=token,
        device_id=device_info.device_id,
        grid_point_coords=grid_point_coords,
        thread_id=thread_id,
        avals=[var.aval for var in input_vars],
        gmem_buffer_keys=input_buffer_keys,
        target_buffer_keys=kernel_input_buffer_keys,
        transforms=(),
    )

    jaxpr_interpreter = jaxpr_interpret.JaxprInterpreter(
        grid_point_coords=grid_point_coords,
        cluster_dims=cluster_dims,
        thread_id=thread_id,
        mesh=mesh,
        device_info=device_info,
        compiler_params=compiler_params,
        interpret_params=interpret_params,
    )
    token, _ = jaxpr_interpreter.interpret(jaxpr, token, *kernel_buffer_keys)

    # Note that a comment about potential races that is analogous to the comment
    # before the call to `_copy_from_gmem_buffers` above applies here too.
    #
    # TODO(nrink): Support copying of slices/blocks only, based on the
    # `BlockSpec`s. (Currently only trivial `BlockSpec`s are supported.)
    token = _copy_to_gmem_buffers(
        token=token,
        device_id=device_info.device_id,
        grid_point_coords=grid_point_coords,
        thread_id=thread_id,
        avals=[var.aval for var in output_vars],
        source_buffer_keys=kernel_output_buffer_keys,
        gmem_buffer_keys=[buffer.key for buffer in output_buffers],
        transforms=(),
    )
    return token

  num_grid_loop_iterations = math.prod(grid_dims)

  def _grid_loop_body(loop_idx: int, token):
    grid_point_coords = interpret_utils.get_indices(
        grid_dims, loop_idx
    )
    token = thread_map.thread_map(
        _kernel,
        math.prod(cluster_dims) * num_threads,
        token,
        grid_point_coords,
        use_ordered_callback=True,
    )
    return token
    # TODO(nrink): Determine if any synchronization between the vector clocks is
    # required at this point, i.e. when a set of concurrent threads is done.

  # Synchronize all clocks before we start launching concurrent threads (in the
  # body of the `fori_loop` below that loops over the grid points).
  token = gpu_callbacks.call_update_clocks_for_device_barrier(
      token, jnp.int32(device_info.device_id)
  )

  # TODO(nrink): For now we execute the grid by sequentially looping over the
  # points in the grid. This may need to be refined to be more faithful to the
  # semantics of grid execution on a real GPU. (The other extreme would be to
  # execute all grid points fully concurrently, e.g. in individual threads.)
  token = jax.lax.fori_loop(0, num_grid_loop_iterations, _grid_loop_body, token)

  # Synchronize all clocks after processing all grid points (i.e. blocks; in the
  # `fori_loop` above). If we do not do this, then reading the output buffers
  # in `_get_outputs` below may lead to races being detected.
  token = gpu_callbacks.call_update_clocks_for_device_barrier(
      token, jnp.int32(device_info.device_id)
  )

  token, outputs = _get_outputs(token, device_info.device_id, output_buffers)

  # We assert that no barriers remain allocated. This is an internal consistency
  # check because the interpreter should take care of deallocating all barriers
  # that it has allocated. It is important that the interpreter deallocates all
  # barriers because barrier deallocation also checks that the barrier was used
  # correctly by the kernel/threads. (Specifically, it is checked that if a
  # thread has observed any completed barrier arrival, it has in fact observed
  # all completed arrivals).
  token = gpu_callbacks.call_assert_no_barriers_allocated(token)

  token = gpu_callbacks.call_clean_up_shared_memory(token)

  callback.io_callback(
      gpu_callbacks.ordering_barrier,
      gpu_callbacks.TOKEN_SHAPE_DTYPE,
      token,
      ordered=True,
  )

  return outputs


def interpret_pallas_call(
    *args,
    jaxpr: jax_core.Jaxpr,
    debug: bool,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: pallas_core.GridMapping,
    mesh: pallas_core.Mesh | None,
    compiler_params: pallas_core.CompilerParams | None,
    cost_estimate: pallas_core.CostEstimate,
    out_avals: tuple[jax_core.AbstractValue, ...],
    interpret_params: InterpretParams,
    metadata: frozen_dict.FrozenDict[str, str] | None,
    name: str | None,
):
  del debug, cost_estimate, out_avals, name
  del metadata  # TODO(sharadmv): Add metadata to HLO.

  if compiler_params is None:
    mosaic_params = mosaic_core.CompilerParams()
  else:
    assert isinstance(compiler_params, mosaic_core.CompilerParams)
    mosaic_params = compiler_params
  del compiler_params

  if isinstance(mesh, mosaic_core.TensorCoreMesh):
    # As a convenience for users, if we are interpreting a pl.core_map over a
    # TensorCoreMesh, we automatically set the number of cores per device so
    # that users don't have to specify it in the InterpretParams.
    assert len(mesh.shape) == 1
    interpret_params = dataclasses.replace(
        interpret_params, num_cores_or_threads=mesh.devices.shape[0]
    )
    # When we're called from mpmp_map, dimension_semantics may not be set.
    if mesh.devices.shape[0] > 1:
      mosaic_params = mosaic_params.replace(dimension_semantics=('parallel',))

  args = [remove_memory_space_p.bind(a) for a in args]
  # args contains: *dynamic_grid_sizes, *index, *inputs.  (No consts?)
  dynamic_grid_args, scalars, input_args = split_list(
      args,
      [grid_mapping.num_dynamic_grid_bounds, grid_mapping.num_index_operands],
  )
  dynamic_grid_args_iter = iter(dynamic_grid_args)
  grid = tuple(
      a if not isinstance(a, pallas_core.DynamicGridDim)
      else next(dynamic_grid_args_iter)
      for a in grid_mapping.grid
  )
  assert next(dynamic_grid_args_iter, None) is None

  axis_sizes = jax_core.get_axis_env().axis_sizes
  num_devices = functools.reduce(
      jnp.multiply, axis_sizes.values(), jnp.int32(1))
  axis_indices : dict[jax_core.AxisName, Array] = {
      k: lax.axis_index(k) for k in axis_sizes.keys()}
  device_id = interpret_utils.device_coords_to_logical_id(
      tuple(axis_indices.values()), axis_sizes, axis_indices
  )

  token = jnp.array(TOP_LEVEL_TOKEN_VALUE, dtype=jnp.int32)

  # We pass our `token` through an ordered IO callback at the start and end of
  # the interpreted kernel, to ensure that execution of this interpreted kernel
  # cannot overlap with the interpretation of any other kernel.
  token = callback.io_callback(
      ordering_barrier, TOKEN_SHAPE_DTYPE, token, ordered=True)

  token = callback.io_callback(
      functools.partial(
          _initialize_shared_memory, interpret_params=interpret_params
      ),
      TOKEN_SHAPE_DTYPE,
      token,
      device_id,
      num_devices,
      interpret_params.num_cores_per_device,
  )

  # Pad input arguments.
  is_squeeze_dim = [
      tuple(isinstance(b, pallas_core.Squeezed) for b in bm.block_shape)
      for bm in grid_mapping.block_mappings
  ]
  block_shapes = [
      pallas_core._get_block_shape(bm.block_shape)
      for bm in grid_mapping.block_mappings
  ]
  num_inputs = grid_mapping.num_inputs
  input_args = [
      interpret_utils.pad_to_block_dimension(
          a, bs, interpret_params.uninitialized_memory)
      for a, bs in zip(input_args, block_shapes[:num_inputs])
  ]

  # Allocate HBM buffers for pallas_call inputs.
  #
  # TODO(jburnim): As an optimization, skip allocating buffers for inputs that
  # are neither aliased nor passed to the kernel in HBM?
  input_buffer_ids = []
  for i, var in enumerate(
      jaxpr.invars[grid_mapping.num_index_operands:][:grid_mapping.num_inputs]):
    assert var.aval.dtype == input_args[i].dtype  # pyrefly: ignore[missing-attribute]
    token, buffer_id = callback.io_callback(
        _allocate_buffer,
        (TOKEN_SHAPE_DTYPE, jax.ShapeDtypeStruct((), jnp.int16)),
        token,
        device_id,
        None,  # local_core_id
        TPU_MEMORY_SPACE_IDXS[mosaic_core.MemorySpace.HBM],
        input_args[i],
    )
    input_buffer_ids.append(buffer_id)

  # Allocate buffers in HBM for pallas_call outputs.
  oi_alias_map = {v: k - len(scalars) for k, v in input_output_aliases}
  if any(i < 0 for i in oi_alias_map.keys()):
    raise ValueError('Aliasing of scalar prefetch arguments is not currently '
                     'supported in TPU interpret mode.')
  output_buffer_ids = []
  output_buffer_shapes = []
  output_vals = []
  num_outputs = grid_mapping.num_outputs
  output_block_shapes = block_shapes[num_inputs : num_inputs + num_outputs]
  for i, bm in enumerate(grid_mapping.block_mappings_output):
    if i in oi_alias_map:
      # Reuse the HBM buffer for the aliased pallas_call input.
      output_buffer_ids.append(input_buffer_ids[oi_alias_map[i]])
      output_buffer_shapes.append(input_args[oi_alias_map[i]].shape)
      output_vals.append(input_args[oi_alias_map[i]])
    else:
      out_val = interpret_utils.get_uninitialized_array(
          bm.array_aval.shape, bm.array_aval.dtype,
          interpret_params.uninitialized_memory)
      padded_val = interpret_utils.pad_to_block_dimension(
          out_val, output_block_shapes[i], interpret_params.uninitialized_memory
      )
      token, buf_id = callback.io_callback(
          _allocate_buffer,
          (TOKEN_SHAPE_DTYPE, jax.ShapeDtypeStruct((), jnp.int16)),
          token,
          device_id,
          None,  # local_core_id
          TPU_MEMORY_SPACE_IDXS[mosaic_core.MemorySpace.HBM],
          padded_val,
      )
      output_buffer_ids.append(buf_id)
      output_buffer_shapes.append(padded_val.shape)
      output_vals.append(out_val)

  # Allocate buffers for non-HBM kernel arguments (e.g., scalars, inputs,
  # outputs, scratch).
  scalar_buffer_ids = []
  for var, val in zip(jaxpr.invars[grid_mapping.slice_index_ops], scalars):
    assert var.aval.shape == val.shape
    assert var.aval.dtype == val.dtype
    token, buf_id = callback.io_callback(
        _allocate_buffer,
        (TOKEN_SHAPE_DTYPE, jax.ShapeDtypeStruct((), jnp.int16)),
        token,
        device_id,
        None,  # local_core_id,
        TPU_MEMORY_SPACE_IDXS[mosaic_core.MemorySpace.SMEM],
        val,
    )
    scalar_buffer_ids.append(buf_id)

  kernel_buffer_ids = scalar_buffer_ids.copy()
  for i, var in enumerate(jaxpr.invars[grid_mapping.num_index_operands:]):
    output_idx = i - grid_mapping.num_inputs
    is_input = i < grid_mapping.num_inputs
    is_output = (output_idx >= 0) and (output_idx < grid_mapping.num_outputs)
    aval = var.aval
    if is_input or is_output:
      memory_space = _forward_any_to_hbm(
          grid_mapping.block_mappings[i].transformed_block_aval.memory_space)
    else:
      memory_space = _forward_any_to_hbm(aval.memory_space)  # pyrefly: ignore[missing-attribute]
    if memory_space is _SEMAPHORE:
      token, sem_id = callback.io_callback(
          _allocate_semaphores,
          (TOKEN_SHAPE_DTYPE, jax.ShapeDtypeStruct(aval.shape, jnp.int16)),  # pyrefly: ignore[missing-attribute]
          token,
          device_id,
          None,  # local_core_id
          aval.shape,  # pyrefly: ignore[missing-attribute]
      )
      kernel_buffer_ids.append(sem_id)
    elif memory_space is _HBM:
      # Use the already-allocated HBM input or output buffer.
      #
      # TODO(jburnim): For kernel args in HBM, check that block shape equals the
      # shape of the corresponding pallas_call input, and that the index_map
      # is trivial.
      assert is_input ^ is_output
      if is_input:
        kernel_buffer_ids.append(input_buffer_ids[i])
      if is_output:
        kernel_buffer_ids.append(output_buffer_ids[output_idx])
    else:
      token, buf_id = callback.io_callback(
          _allocate_buffer,
          (TOKEN_SHAPE_DTYPE, jax.ShapeDtypeStruct((), jnp.int16)),
          token,
          device_id,
          None,  # local_core_id,
          TPU_MEMORY_SPACE_IDXS[memory_space],
          interpret_utils.get_uninitialized_array(
              var.aval.shape,  # pyrefly: ignore[missing-attribute]
              var.aval.dtype,  # pyrefly: ignore[missing-attribute]
              interpret_params.uninitialized_memory,
          ),
      )
      kernel_buffer_ids.append(buf_id)

  if mosaic_params.collective_id is None:
    # The kernel doesn't specify its own barrier semaphore, so we do a global
    # barrier before running the first iteration of the kernel.
    token = callback.io_callback(_barrier, TOKEN_SHAPE_DTYPE, token, device_id)

  _, input_ids, kernel_output_ids, _  = split_list(
      kernel_buffer_ids,
      [grid_mapping.num_index_operands, num_inputs, grid_mapping.num_outputs])
  input_vars, output_vars = split_list(
      jaxpr.invars[grid_mapping.slice_block_ops], [num_inputs])
  input_var_memory_spaces, output_var_memory_spaces = split_list(
      [_forward_any_to_hbm(bm.transformed_block_aval.memory_space)
       for bm in grid_mapping.block_mappings],
      [num_inputs])
  if grid:
    num_iterations = functools.reduce(jnp.multiply, grid)
  else:
    # Base case is always one iteration when grid is ()
    num_iterations = 1

  if isinstance(mesh, mosaic_core.TensorCoreMesh):
    # We are interpreting a pl.core_map over a TensorCoreMesh, so we use a
    # fixed division of the grid between cores, instead of a random division.
    randomized_grid_coordinates = (jnp.array((), dtype=jnp.int32),) * len(grid)
  else:
    randomized_grid_coordinates = _get_randomized_grid_coordinates(
        grid, mosaic_params, interpret_params.random_seed
    )

  parallel_dim_semantics = _get_parallel_dim_semantics(
      mosaic_params, len(grid)
  )
  parallel_subgrid_size = _get_parallel_subgrid_size(
      parallel_dim_semantics, grid
  )
  num_points_in_parallel_subgrid_per_core = (
      parallel_subgrid_size + interpret_params.num_cores_per_device - 1
  ) // interpret_params.num_cores_per_device  # We round up here.
  num_iterations_per_point_in_parallel_subgrid = (
      # This is evenly divisible.
      num_iterations // parallel_subgrid_size
  )
  num_iterations_per_core = (
      num_points_in_parallel_subgrid_per_core
      * num_iterations_per_point_in_parallel_subgrid
  )
  def _get_local_grid_env(grid_point):
    if grid_mapping.local_grid_env is not None:
      return grid_mapping.local_grid_env(grid_point, grid)
    else:
      return tuple(
          pallas_core.GridAxis(idx, b)
          for dim, (idx, b) in enumerate(zip(grid_point, grid))
          if dim not in grid_mapping.vmapped_dims
      )

  def _execute_grid_for_core(core_index, token):
    # NOTE: We assume here that all parallel dimensions appear before all
    # arbitrary dimensions in the grid.  (We will have raised an error earlier
    # if this is not the case.)
    #
    # TODO(jburnim): Are we overusing nested local functions here?
    ctx = InterpretContext(
        grid_mapping=grid_mapping,
        mesh=mesh,
        axis_sizes=axis_sizes,
        axis_indices=axis_indices,  # pyrefly: ignore[bad-argument-type]
        device_id=device_id,
        local_core_id=core_index,
        mosaic_params=mosaic_params,
        interpret_params=interpret_params,
    )

    initial_iteration_idx = core_index * num_iterations_per_core
    loop_bound = jnp.minimum(
        (core_index + 1) * num_iterations_per_core, num_iterations)

    def _body(
        carry: tuple[
            jnp.int32,
            tuple[jnp.int32, ...],
            jnp.ndarray,
            tuple[jnp.ndarray, ...],
            tuple[jnp.ndarray, ...],
            tuple[jnp.ndarray, ...],
            jnp.int32,
        ],
        ctx: InterpretContext,
    ) -> tuple[
        jnp.int32,
        tuple[jnp.int32, ...],
        jnp.ndarray,
        tuple[jnp.ndarray, ...],
        tuple[jnp.ndarray, ...],
        tuple[jnp.ndarray, ...],
        jnp.int32,
    ]:
      """Performs one execution of the kernel body.

      Execution of `jaxpr` is preceded by reading kernel input buffers and
      followed by writing kernel output buffers.

      Args:
        carry: (iteration_idx, loop_idx, grid_point, prev_start_indices,
                cur_start_indices, token).
          - iteration_idx: the iteration index.
          - loop_idx: internal indices for looping over the grid.
          - grid_point: the current positions along all axes of the grid.
          - prev_start_indices: a rank-1 array that contains the start indices
            for the slices of inputs and outputs processed in the previous loop
            iteration.
          - cur_start_indices: a rank-1 array that contains the start indices
            for the slices of inputs and outputs processed in the current loop
            iteration.
          - token: the token we thread through IO callbacks to ensure they are
            executed in order.
        ctx: the InterpretContext.

      Returns:
        The carry for the next iteration.
      """
      (
          iteration_idx,
          loop_idx,
          grid_point,
          prev_start_indices,
          cur_block_indices,
          cur_start_indices,
          token,
      ) = carry
      ctx = ctx.replace(
          grid_point=grid_point, local_core_id=core_index)
      if interpret_params.grid_point_recorder is not None:
        token = callback.io_callback(
            interpret_params.grid_point_recorder,
            TOKEN_SHAPE_DTYPE,
            token,
            grid_point,
            core_index,
        )

      with pallas_core.grid_env(_get_local_grid_env(grid_point)):
        next_loop_idx = interpret_utils.get_next_indices(grid, loop_idx)
        next_grid_point = _get_grid_point(
            next_loop_idx, randomized_grid_coordinates
        )
        next_block_indices = []
        next_start_indices = []
        for bm in grid_mapping.block_mappings:
          token, block_indices, start_indices = _compute_start_indices(
              bm, next_grid_point, *scalar_buffer_ids, ctx=ctx, token=token
          )
          next_block_indices.append(block_indices)
          next_start_indices.append(start_indices)
        if jaxpr.debug_info.arg_names is not None:
          input_names, output_names = split_list(
            jaxpr.debug_info.arg_names[grid_mapping.slice_block_ops], [num_inputs])
        else:
          input_names = ["unknown",] * grid_mapping.num_inputs
          output_names = ["unknown",] * grid_mapping.num_outputs

        # Copy slices of the input to the kernel buffers.
        def _store_slice_to_kernel_input(index, input_var, memory_space, token):
          # Copy from the HBM buffer for the pallas_call input to the kernel
          # input buffer.
          # TODO(jburnim): Just use input_args[j] when the input is not aliased?
          transform = indexing.NDIndexer(
              indices=tuple(
                  indexing.Slice(st, sz) if not iid else st
                  for st, sz, iid in zip(
                      cur_start_indices[index],
                      block_shapes[index],
                      is_squeeze_dim[index],
                  )
              ),
              shape=input_args[index].shape,
              int_indexer_shape=(),
          )
          token, sliced_val = callback.io_callback(
              # TODO(jburnim): Pass source_info from the pallas_call, in case this
              # read is involved in a data race.
              functools.partial(get, input_name=input_names[index]),
              (
                  TOKEN_SHAPE_DTYPE,
                  jax.ShapeDtypeStruct(
                      input_var.aval.shape, input_var.aval.dtype
                  ),
              ),
              token,
              device_id,
              core_index,
              TPU_MEMORY_SPACE_IDXS[mosaic_core.MemorySpace.HBM],
              input_buffer_ids[index],
              (transform,),
              cur_block_indices[index],
              grid_point,
          )
          token = callback.io_callback(
              # TODO(jburnim): Pass source_info from the pallas_call, in case this
              # store is involved in a data race.
              store,
              TOKEN_SHAPE_DTYPE,
              token,
              device_id,
              core_index,
              TPU_MEMORY_SPACE_IDXS[memory_space],
              input_ids[index],
              (),
              sliced_val,
          )
          return token

        for j, var in enumerate(input_vars):
          if input_var_memory_spaces[j] is _HBM:
            if var.aval.shape != block_shapes[j]:
              raise ValueError(
                  f'Kernel input {j} in HBM but does not have trivial'
                  ' BlockSpec.'
              )
            continue
          assert len(cur_start_indices[j].shape) == 1
          assert len(prev_start_indices[j].shape) == 1
          token = jax.lax.cond(
              (iteration_idx == initial_iteration_idx)
              | jax.lax.reduce_or(
                  cur_start_indices[j] != prev_start_indices[j], axes=(0,)
              ),
              functools.partial(
                  _store_slice_to_kernel_input,
                  j,
                  var,
                  input_var_memory_spaces[j],
              ),
              lambda t: t,
              token,
          )

        # Invoke the kernel body.
        token, _ = _interpret_jaxpr(
            jaxpr, *kernel_buffer_ids, ctx=ctx, token=token
        )

        # Copy from the kernel buffers to slices of the output in HBM.
        def _store_to_output_buffer(
            index, output_var, transform, memory_space, token
        ):
          token, kernel_output_val = callback.io_callback(
              # TODO(jburnim): Pass source_info from the pallas_call, in case this
              # get is involved in a data race.
              get,
              (TOKEN_SHAPE_DTYPE, output_var.aval),
              token,
              device_id,
              core_index,
              TPU_MEMORY_SPACE_IDXS[memory_space],
              kernel_output_ids[index],
              (),
          )
          token = callback.io_callback(
              # TODO(jburnim): Pass source_info from the pallas_call, in case this
              # store is involved in a data race.
              functools.partial(store, output_name=output_names[index]),
              TOKEN_SHAPE_DTYPE,
              token,
              device_id,
              core_index,
              TPU_MEMORY_SPACE_IDXS[mosaic_core.MemorySpace.HBM],
              output_buffer_ids[index],
              (transform,),
              kernel_output_val,
              cur_block_indices[num_inputs + index],
              grid_point,
          )
          return token

        output_slices : list[Any] = []
        for j, var in enumerate(output_vars):
          if output_var_memory_spaces[j] is _HBM:
            if var.aval.shape != block_shapes[num_inputs + j]:
              raise ValueError(
                  f'Kernel output {j} in HBM but does not have trivial'
                  ' BlockSpec.'
              )
            output_slices.append(None)
            continue
          assert len(cur_start_indices[num_inputs + j].shape) == 1
          assert len(next_start_indices[num_inputs + j].shape) == 1
          transform = indexing.NDIndexer(
              indices=tuple(  # pyrefly: ignore[bad-argument-type]
                  indexing.ds(st, sz) if not iid else st  # pyrefly: ignore[bad-argument-type]
                  for st, sz, iid in zip(
                      cur_start_indices[num_inputs + j],
                      block_shapes[num_inputs + j],
                      is_squeeze_dim[num_inputs + j],
                  )
              ),
              shape=output_vals[j].shape,
              int_indexer_shape=(),
          )
          if j in oi_alias_map:
            # Suppress revisiting check for output buffers that are aliased to
            # input buffers.
            output_slices.append(None)
          else:
            output_slices.append((transform,))
          token = jax.lax.cond(
              (iteration_idx + 1 == loop_bound)
              | jax.lax.reduce_or(
                  cur_start_indices[num_inputs + j]
                  != next_start_indices[num_inputs + j],
                  axes=(0,),
              ),
              functools.partial(
                  _store_to_output_buffer,
                  j,
                  var,
                  transform,
                  output_var_memory_spaces[j],
              ),
              lambda t: t,
              token,
          )
        token = callback.io_callback(
            _check_for_revisiting,
            TOKEN_SHAPE_DTYPE,
            token,
            device_id,
            core_index,
            loop_idx,
            output_slices,
        )

        ret_carry = (
            iteration_idx + 1,
            next_loop_idx,
            next_grid_point,
            cur_start_indices,
            tuple(next_block_indices),
            tuple(next_start_indices),
            token,
        )
        return ret_carry

    initial_loop_idx = interpret_utils.get_indices(grid, initial_iteration_idx)
    initial_grid_point = _get_grid_point(
      initial_loop_idx, randomized_grid_coordinates)
    with pallas_core.grid_env(_get_local_grid_env(initial_grid_point)):
      initial_block_indices = []
      initial_start_indices = []
      for bm in grid_mapping.block_mappings:
        token, block_indices, start_indices = _compute_start_indices(
            bm, initial_grid_point, *scalar_buffer_ids, ctx=ctx, token=token
        )
        initial_block_indices.append(block_indices)
        initial_start_indices.append(start_indices)
      initial_block_indices = tuple(initial_block_indices)
      initial_start_indices = tuple(initial_start_indices)

    final_carry = lax.while_loop(
        lambda carry: carry[0] < loop_bound,
        functools.partial(_body, ctx=ctx),
        (
            initial_iteration_idx,
            initial_loop_idx,
            initial_grid_point,
            initial_start_indices,  # Previous start indices are ignored on the first iteration.
            initial_block_indices,
            initial_start_indices,
            token,
        ),
    )
    return final_carry[-1]

  # TODO(jburnim): Should we only create happens-before here from core 0 to
  # the other cores?
  token = callback.io_callback(
      _update_clocks_for_device_barrier, TOKEN_SHAPE_DTYPE, token, device_id
  )

  if interpret_params.num_cores_per_device == 1:
    token = _execute_grid_for_core(jnp.int32(0), token)
  else:
    token = thread_map(
        _execute_grid_for_core,
        interpret_params.num_cores_per_device,
        token,
        device_id=device_id,
        on_exception=fail)

  # TODO(jburnim): Should we only create happens-before here from the other
  # # cores to core 0?
  token = callback.io_callback(
      _update_clocks_for_device_barrier, TOKEN_SHAPE_DTYPE, token, device_id
  )

  # Read the output from the allocated output buffers.
  ret = []
  for val, output_buffer_id, output_buffer_shape in zip(
      output_vals, output_buffer_ids, output_buffer_shapes
  ):
    token, r = callback.io_callback(
        # TODO(jburnim): Pass source_info from the pallas_call, in case this
        # get is involved in a data race.
        get,
        (TOKEN_SHAPE_DTYPE, val),
        token,
        device_id,
        0,  # local_core_id
        TPU_MEMORY_SPACE_IDXS[mosaic_core.MemorySpace.HBM],
        output_buffer_id,
        (
            indexing.NDIndexer.from_indices_shape(
                tuple(indexing.ds(0, s) for s in val.shape),
                output_buffer_shape,
            ),
        ),
    )
    ret.append(r)

  token = callback.io_callback(_validate, TOKEN_SHAPE_DTYPE, token, device_id)

  # For now, when we're done with a pallas_call, we delete the shared memory.
  # We use a barrier to ensure that all devices are done running the kernel.
  #
  # TODO(jburnim): Get rid of this barrier.  And figure out how this should
  # work if we want to invoke successive pallas_calls that use the same
  # shared memory.
  token = callback.io_callback(
      _clean_up_shared_memory, TOKEN_SHAPE_DTYPE, token, device_id)

  callback.io_callback(
      ordering_barrier, TOKEN_SHAPE_DTYPE, token, ordered=True)

  return ret

