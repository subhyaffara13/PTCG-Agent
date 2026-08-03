from typing import Any

def sort_depths(
    args: tuple[Any, ...], depth_map: dict[fx.Node, int]
) -> list[tuple[fx.Node, int]]:
    arg_depths = {
        arg: depth_map[arg] for arg in args if isinstance(arg, torch.fx.node.Node)
    }
    return sorted(arg_depths.items(), key=operator.itemgetter(1), reverse=True)

