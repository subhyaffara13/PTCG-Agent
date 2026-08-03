from typing import Any

def wrap_bound_arg(
    tx: "InstructionTranslator", val: Any, source: Source | None = None
) -> VariableTracker:
    # Source propagation is best effort since not every object we encounter has a source to begin with.
    if isinstance(val, VariableTracker):
        return val
    elif not source:
        return VariableTracker.build(tx, val)
    else:
        # Create a lazy variable to avoid guarding on __defaults__ unless really
        # needed.
        return variables.LazyVariableTracker.create(val, source)

