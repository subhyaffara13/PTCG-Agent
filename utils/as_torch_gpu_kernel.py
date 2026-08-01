
def as_torch_gpu_kernel(
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
    thread_semantics: LoweringSemantics = LoweringSemantics.Lane,
    inout_shape=(),
):
  (
      module,
      in_shape,
      inout_shape,
      out_shape,
      unwrap_output_tuple,
      is_device_collective,
  ) = _kernel_to_module(
      body,
      grid,
      block,
      in_shape,
      out_shape,
      smem_scratch_shape,
      prof_spec,
      cluster,
      module_name,
      kernel_name,
      thread_semantics,
      inout_shape,
  )
  module = _run_serde_pass(module, serialize=True, ir_version=None)
  bytecode_buffer = io.BytesIO()
  module.operation.write_bytecode(bytecode_buffer)
  return _as_torch_gpu_kernel(
      bytecode_buffer.getvalue(),
      in_shape,
      out_shape,
      inout_shape,
      unwrap_output_tuple=unwrap_output_tuple,
  )

