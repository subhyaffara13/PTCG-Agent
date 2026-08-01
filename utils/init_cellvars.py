
def init_cellvars(
    parent: "InstructionTranslator",
    result: dict[str, VariableTracker],
    code: types.CodeType,
) -> None:
    """
    Update `result` to add mapping from local name to new cells created
    directly by `code`, or update SideEffects in `parent` if the a local cell is
    already in `result` (cell argument).
    """
    side_effects = parent.output.side_effects

    for name in code.co_cellvars:
        new_cell = side_effects.track_cell_new()
        if name in result:
            # This handles when a function argument is a cell (e.g., captured by
            # a nested func). See `MAKE_CELL` bytecode for more info.
            side_effects.store_cell(new_cell, result.pop(name))
        result[name] = new_cell

