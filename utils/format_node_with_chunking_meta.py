
def format_node_with_chunking_meta(
    node: torch.fx.Node, include_args: bool = False
) -> None:
    """
    Print the node with chunking metadata for the current node if exists.

    If include_args is True, also print chuning metadata for Node arguments.
    """
    from torch._inductor.runtime.runtime_utils import green_text

    from .core import get_chunking_meta

    fake_tensor = get_fake_tensor_from_node_arg(node)
    shape = list(fake_tensor.shape) if fake_tensor is not None else "?"
    print(f"  {shape} {node.format_node()}")

    if meta := get_chunking_meta(node):
        print(f"    {green_text(str(meta))}")

    if include_args:
        for arg in get_args_of_node_type(node):
            if arg_meta := get_chunking_meta(arg):
                print(f"    {arg}: {green_text(str(arg_meta))}")

