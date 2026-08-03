from typing import Any

def register_pytree_flatten_spec(
    cls: type[Any],
    flatten_fn_spec: FlattenFnSpec,
    flatten_fn_exact_match_spec: FlattenFnExactMatchSpec | None = None,
) -> None:
    SUPPORTED_NODES[cls] = flatten_fn_spec
    SUPPORTED_NODES_EXACT_MATCH[cls] = flatten_fn_exact_match_spec

