from typing import Union

def _kernel_to_module(
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
    inout_shape = (),
):
  if isinstance(in_shape, list):
    in_shape = tuple(in_shape)
  elif not isinstance(in_shape, tuple):
    in_shape = (in_shape,)
  if isinstance(inout_shape, list):
    inout_shape = tuple(inout_shape)
  elif not isinstance(inout_shape, tuple):
    inout_shape = (inout_shape,)
  if kernel_name is None:
    kernel_name = jax_util.fun_name(body, "anonymous")

  inout_shape = jax.tree.map(jax.ShapeDtypeStruct.like, inout_shape)
  out_shape = jax.tree.map(jax.ShapeDtypeStruct.like, out_shape)
  jax_mesh = mesh_lib.get_concrete_mesh()
  if jax_mesh.empty:
    jax_mesh = mesh_lib.thread_resources.env.physical_mesh
  module, out_shape, unwrap_output_tuple, launch_ctx = (
      _lower_as_gpu_kernel(
          body, grid, cluster, block, in_shape, out_shape, inout_shape,
          smem_scratch_shape, thread_semantics, module_name, kernel_name,
          prof_spec, jax_mesh=jax_mesh
      )
  )

  if thread_semantics == LoweringSemantics.Warpgroup and dialect is not None:
    # We need to run a pass that removes dead-code for which layout inference
    # does not work.
    pm = mlir.passmanager.PassManager.parse("builtin.module(canonicalize)", module.context)
    pm.run(module.operation)

    # Run Python lowering passes. The remaining passes will be run in C++ in
    # jax/jaxlib/mosaic/gpu/custom_call.cc
    layout_inference.infer_layout(module, arch=_infer_arch())
    dialect_lowering.lower_mgpu_dialect(module, launch_ctx)

  launch_ctx.scratch.finalize_size()
  module.operation.verify()

  return (
      module,
      in_shape,
      inout_shape,
      out_shape,
      unwrap_output_tuple,
      launch_ctx.is_device_collective,
  )

