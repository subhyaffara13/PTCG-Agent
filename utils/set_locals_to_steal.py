from typing import Any

def set_locals_to_steal(gm: torch.fx.GraphModule, locals_to_steal: list[Any]) -> None:
    gm.meta["locals_to_steal"] = locals_to_steal

