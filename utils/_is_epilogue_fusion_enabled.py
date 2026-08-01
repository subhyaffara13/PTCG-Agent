
def _is_epilogue_fusion_enabled(template_node: BaseSchedulerNode) -> bool:
    """Check per-template flag, fall back to global config."""
    tb = template_node.get_template_node()
    if tb is not None and tb.allow_epilogue_fusion is not None:
        return tb.allow_epilogue_fusion
    return config.epilogue_fusion

