from typing import Any

def serialize_pytreedef(node) -> dict[str, Any]:
  builder = flatbuffers.Builder(65536)
  exported = _serialize_pytreedef(builder, node)
  builder.Finish(exported)
  root_repr = base64.b64encode(builder.Output()).decode("utf-8")
  leaf_count = node.num_leaves
  pytree_repr = {_TREE_REPR_KEY: root_repr,
                 _LEAF_IDS_KEY: list(range(leaf_count))}
  return pytree_repr

