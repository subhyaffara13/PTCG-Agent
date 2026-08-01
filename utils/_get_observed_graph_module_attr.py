
def _get_observed_graph_module_attr(
    model: torch.nn.Module | GraphModule, attr_name: str
) -> Any:
    if hasattr(model, "meta") and "_observed_graph_module_attrs" in model.meta:  # type: ignore[operator, index]
        return getattr(model.meta["_observed_graph_module_attrs"], attr_name)  # type: ignore[index]
    return None

