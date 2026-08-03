import json
import pathlib

def load_pytreedef(directory: str | PathLike[str]) -> PyTreeT:
  """Loads a pytree from the given directory.

  This is a simple experimental array serialization API, for anything more
  complex and for all checkpointing prefer: https://github.com/google/orbax

  Args:
    directory: Directory path to load from.
  Returns:
    The loaded pytree with arrays represented as jax.ShapeDtypeStruct's.
  """
  assert not _is_remote_path(directory) or pathlib.epath_installed, (
    "For checkpointing using remote URLs (e.g., gs, s3) you need `etils`"
    " module installed. You can install it using `pip install etils`.")
  json_content = (_norm_path(directory) / _PYTREEDEF_FILE).read_text()
  raw_tree = json.loads(json_content)
  leaves = map(_desc_to_leaf, raw_tree[utils._LEAF_IDS_KEY])
  return jax.tree.unflatten(utils.deserialize_pytreedef(raw_tree), leaves)

