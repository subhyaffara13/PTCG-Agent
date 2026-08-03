from typing import Any

def _get_fake_tensor(vt: VariableTracker) -> Any:
    fake_tensor = vt.as_proxy().node.meta.get("example_value")
    if not is_fake(fake_tensor):
        from . import graph_break_hints
        from .exc import unimplemented

        unimplemented(
            gb_type="Cannot check Tensor object identity without its fake value",
            context=str(fake_tensor),
            explanation="TensorVariable is missing a fake example_value.",
            hints=[*graph_break_hints.DYNAMO_BUG],
        )
    return fake_tensor

