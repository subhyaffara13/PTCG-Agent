import logging
from typing import Any

def log_pytree(msg: str, pytree: Any):
  """Logs the pytree in a pretty format."""
  jax.tree.map_with_path(
      lambda path, x: logging.info(
          "%r path: %r: %r, spec=%r, mesh=%r,\nvalue=%r\n dtype=%r",
          msg,
          path,
          x.shape,
          x.sharding.spec,
          x.sharding.mesh,
          [shard.data for shard in x.addressable_shards],
          x.dtype if hasattr(x, "dtype") else None,
      ),
      pytree,
  )

