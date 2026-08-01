
def set_reuse_ir(val: bool) -> None:
    """Set the config to reuse IR nodes for faster tracing"""
    torch._C._lazy._set_reuse_ir(val)

