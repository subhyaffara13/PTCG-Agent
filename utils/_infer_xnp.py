
def _infer_xnp(
    xnps: dict[numpy_utils.NpModule, list[str]]
) -> numpy_utils.NpModule:
  """Extract the `xnp` module."""
  non_np_xnps = set(xnps) - {np}  # jnp, tnp, torch take precedence on `np`

  # Detecting conflicting xnp
  if len(non_np_xnps) > 1:
    xnps = {k.__name__: v for k, v in xnps.items()}
    raise ValueError(f'Conflicting numpy types: {xnps}')

  if not non_np_xnps:
    return np
  else:
    (xnp,) = non_np_xnps
    return xnp

