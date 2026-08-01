
def assert_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    if len(n.users) != 0:
        raise AssertionError(f"Expected no users, got {len(n.users)}")
    return [], counter  # pyrefly: ignore[implicit-any]

