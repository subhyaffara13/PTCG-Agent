
def lower_as_mlir(
    f,
    *args,
    dynamic_shapes=False,
    device=None,
    static_argnames=(),
    platforms=None,
    **kwargs,
) -> str:
  """Lower the function to MLIR.

  Unlike jax.export, the exported artifact provides no stability guarantees.
  """
  with pallas_export_experimental(dynamic_shapes):
    f = jit(f, device=device, static_argnames=static_argnames)
    if platforms is None:
      platforms = ["tpu"]
    exported = export(f, platforms=platforms)(*args, **kwargs)
    return exported.mlir_module()

