
def _print_override_graphs(*, print_inactive: bool = False) -> None:
    """
    Print all override graphs for debugging purposes.

    Args:
        print_inactive: Whether to print inactive nodes
    """
    for (op, key), node_list in _graphs.items():
        print(f"{op=}, {key=}")

        for i, node in enumerate(node_list):
            if node.active or print_inactive:
                s: str = f"    {i}: {node.dsl_name=}, {node.unconditional_override=}"
                if print_inactive:
                    s += f" {node.active=}"

                print(s)

