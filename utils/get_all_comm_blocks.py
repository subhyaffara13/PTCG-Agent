from typing import Callable

def get_all_comm_blocks(
    graph: fx.Graph,
    comm_ops: tuple[torch._ops.OpOverload, ...],
    comm_filter: Callable[..., bool] | None = None,
) -> list[CommBlock]:
    if comm_filter is None:

        def always_true(comm_block: CommBlock) -> bool:
            return True

        comm_filter = always_true

    blocks = []
    for node in graph.nodes:
        if node.target not in comm_ops:
            continue
        comm_block = get_comm_block(node)
        if comm_block is not None and comm_filter(comm_block):
            blocks.append(comm_block)
    return blocks

