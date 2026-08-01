
def get_locals_to_steal(maybe_gm: Any) -> list[Any]:
    if not isinstance(maybe_gm, torch.fx.GraphModule) or not hasattr(maybe_gm, "meta"):
        return []
    return maybe_gm.meta.get("locals_to_steal", [])

