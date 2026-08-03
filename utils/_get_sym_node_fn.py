from typing import Callable

def _get_sym_node_fn(name: str) -> Callable[[SymNode], SymNode]:
    def fn(self: SymNode) -> SymNode:
        return getattr(self, f"_sym_{name}")()

    return fn

