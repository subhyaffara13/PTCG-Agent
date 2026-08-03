from typing import Callable

def return_arg_list(arg_indices: list[int]) -> Callable[[Node], list[int]]:
    """
    Constructs a function that takes a node as arg and returns the arg_indices
    that are valid for node.args
    """

    def arg_indices_func(node: Node) -> list[int]:
        return [i for i in arg_indices if i < len(node.args)]

    return arg_indices_func

