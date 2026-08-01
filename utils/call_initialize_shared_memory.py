
def call_initialize_shared_memory(
    *,
    token: jax.Array,
    num_gpus: jax.Array,
    num_threads_per_block: jax.Array,
    num_blocks_per_cluster: jax.Array,
    interpret_params: InterpretGPUParams,
):
  return callback.io_callback(
      functools.partial(
          _initialize_shared_memory,
          interpret_params=interpret_params,
      ),
      TOKEN_SHAPE_DTYPE,
      token=token,
      num_gpus=num_gpus,
      num_threads_per_block=num_threads_per_block,
      num_blocks_per_cluster=num_blocks_per_cluster,
  )

