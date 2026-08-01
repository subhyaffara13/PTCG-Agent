
def get_current_node() -> torch.fx.Node | None:
    return getattr(_current_node, "value", None)

