import logging
from typing import Any

def _fuse_keys(
    params_dict: dict[str, Any],
    keys_to_fuse: Sequence[str],
    fused_key: str,
    axis: int,
) -> None:
  """Fuses values of keys_to_fuse into fused_key in params_dict."""
  vals_to_fuse = [params_dict[k] for k in keys_to_fuse]

  if all(_is_host_array(x) for x in vals_to_fuse):
    logging.info("DEBUG: Fusing %s on CPU", fused_key)
    # Force concatenation on CPU using JAX to avoid touching TPU
    fused_val = _cpu_concat(vals_to_fuse, axis=axis)
  else:
    is_numpy = isinstance(vals_to_fuse[0], np.ndarray)
    concat_fn = np.concatenate if is_numpy else jnp.concatenate
    fused_val = concat_fn(vals_to_fuse, axis=axis)

  for k in keys_to_fuse:
    del params_dict[k]
  params_dict[fused_key] = fused_val

