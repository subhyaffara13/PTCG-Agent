from typing import Any, Callable

def call_function(
    graph: fx.Graph,
    target: str | Callable[..., Any],
    args: tuple[fx.node.Argument, ...] | None = None,
    kwargs: dict[str, fx.node.Argument] | None = None,
) -> fx.Node:
    # We accept target as a str to avoid typing error as the type of
    # a node.target is str | Callable[..., Any].
    # This also allows us to avoid writing check for every call.
    if isinstance(target, str):
        raise RuntimeError(f"Call function should not get a str target {target=}")
    node = graph.call_function(target, args, kwargs)
    _, args, kwargs = get_fake_args_kwargs(node)
    with V.fake_mode:
        node.meta["val"] = target(*args, **kwargs)
        # node.meta["val"] may be a container. So we use tree_map here
        # to recursively extract the tensor metadata.
        node.meta["tensor_meta"] = tree_map(
            _extract_tensor_metadata, (node.meta["val"],)
        )[0]
    return node

