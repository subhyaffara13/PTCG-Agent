from typing import Any

def is_tensorstore_spec_leaf(leaf: Any):
  # TODO(rdyro): think of a better way to detect which leaf is a ts config
  return leaf is None or (isinstance(leaf, dict)
                          and ("driver" in leaf or "kvstore" in leaf))

