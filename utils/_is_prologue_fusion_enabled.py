
def _is_prologue_fusion_enabled(template_node: BaseSchedulerNode) -> bool:
    """Check per-template flag, fall back to global config."""
    tb = template_node.get_template_node()
    if tb is not None and tb.allow_prologue_fusion is not None:
        return tb.allow_prologue_fusion
    return config.prologue_fusion

