
def as_gpu_kernel(
    body,
    grid: tuple[int, int, int],
    block: tuple[int, int, int],
    in_shape,
    out_shape,
    smem_scratch_shape: ShapeTree | Union[ShapeTree],
    prof_spec: profiler.ProfilerSpec | None = None,
    cluster: tuple[int, int, int] = (1, 1, 1),
    module_name: str = "unknown",
    kernel_name: str | None = None,
    ir_version: int | None = None,
    thread_semantics: LoweringSemantics = LoweringSemantics.Lane,
    inout_shape = (),
):
  module, in_shape, inout_shape, out_shape, unwrap_output_tuple, is_device_collective = _kernel_to_module(
      body, grid, block, in_shape, out_shape, smem_scratch_shape, prof_spec,
      cluster, module_name, kernel_name, thread_semantics, inout_shape
  )

  expected_arg_tys, expected_arg_treedef = jax.tree.flatten((*in_shape, *inout_shape))
  def _check_args(*args):
    arg_treedef = jax.tree.structure(args)
    if arg_treedef != expected_arg_treedef:
      raise ValueError(
          f"Invalid argument structure: expected {expected_arg_treedef}, got"
          f" {arg_treedef}, ({args=})"
      )
    for arg, expected_ty in zip(args, expected_arg_tys):
      if arg.shape != expected_ty.shape:
        raise ValueError(
            f"Argument shape mismatch: expected {expected_ty.shape}, got"
            f" {arg.shape}"
        )
      if arg.dtype != expected_ty.dtype:
        hint = ""
        if not arg.shape:
          hint = f". Hint: cast the scalar to {expected_ty.dtype} explicitly."
        raise ValueError(
            f"Argument dtype mismatch: expected {expected_ty.dtype}, got"
            f" {arg.dtype}{hint}"
        )

  def bind(*args) -> Any:
    return mosaic_gpu_p.bind(
        *args,
        module=module,
        out_types=out_shape,
        inout_types=inout_shape,
    )

  if prof_spec is not None:
    @jax.jit
    def prof_kernel(*args):
      _check_args(*args)
      *results, prof_buffer = bind(*args)
      def dump_profile(prof_buffer):
        out_file = os.path.join(prof_spec.dump_path, f"{time.time_ns()}-trace.json")
        try:
          with open(out_file, "x") as f:
            prof_spec.dump(prof_buffer, f, grid=grid, block=block)
        except FileExistsError:
          pass  # TODO: Retry
      jax.debug.callback(dump_profile, prof_buffer)
      return results[0] if unwrap_output_tuple else results
    return prof_kernel
  else:
    @jax.jit
    def kernel(*args):
      _check_args(*args)
      results = bind(*args)
      return results[0] if unwrap_output_tuple else results
    return kernel

