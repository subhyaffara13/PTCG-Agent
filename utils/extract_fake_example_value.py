from typing import Any

def extract_fake_example_value(node: torch.fx.Node, required: bool = True) -> Any:
    if "example_value" in node.meta and is_fake(node.meta["example_value"]):
        return node.meta["example_value"]
    elif required:
        from torch._dynamo.exc import unimplemented

        from . import graph_break_hints

        unimplemented(
            gb_type="Missing FakeTensor example value",
            context=str(node),
            explanation=f"`FakeTensor` example value was required for {node} but not available.",
            hints=[*graph_break_hints.DYNAMO_BUG],
        )
    else:
        return None

