
def fail_merge_overload(state: State, node: IfStmt) -> None:
    """Report an error when overloads cannot be merged due to unknown condition."""
    state.add_error(
        message_registry.FAILED_TO_MERGE_OVERLOADS.value,
        node.line,
        node.column,
        blocker=False,
        code="misc",
    )

