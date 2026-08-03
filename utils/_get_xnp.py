from typing import Any

def _get_xnp(
    array_args: dict[str, Any],
    *,
    strict: bool,
) -> numpy_utils.NpModule:
  """Extract the xnp module common to the args."""

  xnps = collections.defaultdict(list)
  for k, v in array_args.items():
    try:
      xnps[numpy_utils.lazy.get_xnp(v, strict=strict)].append(k)
    except Exception as e:  # pylint: disable=broad-except
      epy.reraise(e, prefix=f'Invalid {k}: Expected xnp.ndarray: ')

  return _infer_xnp(xnps)

