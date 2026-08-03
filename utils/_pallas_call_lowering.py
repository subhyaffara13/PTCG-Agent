from typing import Any

def _pallas_call_lowering(
    ctx: mlir.LoweringRuleContext, *in_nodes, interpret: Any, **params
):
  if params['jaxpr'].constvars:
    raise ValueError('Cannot lower a pallas_call with constants.')
  if interpret:
    impl = partial(hlo_interpreter.pallas_call_hlo_interpret, **params)

    try:
      from jax._src.pallas.mosaic.interpret import interpret_pallas_call as mosaic_tpu_interpret  # pyrefly: ignore[missing-import]
      from jax._src.pallas.mosaic.interpret import params as tpu_params  # pyrefly: ignore[missing-import]
    except ImportError:
      pass
    else:
      if isinstance(interpret, tpu_params.InterpretParams):
        impl = partial(
            mosaic_tpu_interpret.interpret_pallas_call,
            interpret_params=interpret,
            **params,
        )

    try:
      from jax._src.pallas.mosaic_gpu.interpret import interpret_pallas_call as mosaic_gpu_interpret  # pyrefly: ignore[missing-import]
      from jax._src.pallas.mosaic_gpu.interpret import params as gpu_params  # pyrefly: ignore[missing-import]
    except ImportError:
      pass
    else:
      if isinstance(interpret, gpu_params.InterpretGPUParams):
        impl = partial(
            mosaic_gpu_interpret.interpret_pallas_call,
            interpret_params=interpret,
            **params,
        )

    return mlir.lower_fun(impl, multiple_results=True)(ctx, *in_nodes)

  def cpu_lowering(
      ctx: mlir.LoweringRuleContext,
      *in_nodes: ir.Value | Sequence[ir.Value],
      **params,
  ):
    raise ValueError("Only interpret mode is supported on CPU backend.")

  def tpu_lowering(
      ctx: mlir.LoweringRuleContext,
      *in_nodes: ir.Value | Sequence[ir.Value],
      **params,
  ):
    compiler_params = params.get("compiler_params")
    if compiler_params is not None:
      rule = pallas_core.get_lowering_rule(type(compiler_params), "tpu")
      if rule is not None:
        return rule(ctx, *in_nodes, **params)

    try:
      from jax._src.pallas.mosaic import pallas_call_registration as mosaic_tpu_backend  # pyrefly: ignore[missing-import]
    except ImportError:
      raise _unsupported_lowering_error("tpu") from None

    return mosaic_tpu_backend.pallas_call_tpu_lowering_rule(
        ctx, *in_nodes, **params
    )

  def gpu_lowering(
      ctx: mlir.LoweringRuleContext,
      *in_nodes: ir.Value | Sequence[ir.Value],
      is_rocm: bool,
      compiler_params: pallas_core.CompilerParams | None,
      **params,
  ):
    """Shared GPU lowering implementation for CUDA and ROCm."""
    if compiler_params is not None:
      rule = pallas_core.get_lowering_rule(type(compiler_params), "gpu")
      if rule is not None:
        return rule(ctx, *in_nodes, compiler_params=compiler_params, **params)

    backend: Any = None

    try:
      from jax._src.pallas.mosaic_gpu import core as mgpu_core  # pyrefly: ignore[missing-import]
      from jax._src.pallas.mosaic_gpu import pallas_call_registration as mosaic_gpu_backend  # pyrefly: ignore[missing-import]
    except ImportError:
      pass
    else:
      if (
          isinstance(compiler_params, mgpu_core.CompilerParams)
          or (compiler_params is None and
              config.jax_pallas_use_mosaic_gpu.value)
      ):
        backend = mosaic_gpu_backend

      if backend is mosaic_gpu_backend:
        if is_rocm:
          raise ValueError(
              "Mosaic GPU does not yet support AMD ROCm devices. "
              "Use ``compiler_params=pltriton.CompilerParams()`` for ROCm."
          )

        if ctx.primitive is pallas_call_p:
          deprecations.warn(
              "jax-pallas-call-mgpu",
              "Using ``pl.pallas_call`` for Mosaic GPU kernels is deprecated."
              " Support for that will be removed in a future JAX version."
              " Please migrate to ``plgpu.kernel``.",
              stacklevel=2,
          )

    try:
      from jax._src.pallas.triton import core as triton_core  # pyrefly: ignore[missing-import]
      from jax._src.pallas.triton import pallas_call_registration as triton_backend  # pyrefly: ignore[missing-import]
    except ImportError:
      pass
    else:
      if (
          isinstance(compiler_params, triton_core.CompilerParams)
          or (compiler_params is None and
              not config.jax_pallas_use_mosaic_gpu.value)
      ):
        backend = triton_backend

    if backend is None:
      raise _unsupported_lowering_error("gpu")

    return backend.pallas_call_lowering(
        ctx, *in_nodes, compiler_params=compiler_params, **params
    )

  return mlir.lower_per_platform(
      ctx,
      "pallas_call",
      dict(
          cpu=cpu_lowering,
          tpu=tpu_lowering,
          cuda=partial(gpu_lowering, is_rocm=False),
          rocm=partial(gpu_lowering, is_rocm=True),
      ),
      None,  # default_rule
      effects.no_effects,
      *in_nodes,
      interpret=interpret,
      **params,
  )

