from typing import Any

def raise_on_overridden_hash(obj: Any, vt: VariableTracker) -> None:
    from . import graph_break_hints
    from .exc import unimplemented

    is_overridden = type(obj).__dict__.get("__hash__", False)

    if is_overridden:
        unimplemented(
            gb_type="User-defined object with overridden __hash__",
            context=f"hashing object of type={type(obj)} and variable tracker {vt}",
            explanation=f"Found a user-defined object {vt} with overridden __hash__ when attempting to hash it",
            hints=[
                "Dynamo does not support hashing user-defined objects with overridden __hash__",
                *graph_break_hints.SUPPORTABLE,
            ],
        )

