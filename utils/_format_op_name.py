
def _format_op_name(opinfo_name: str) -> str:
    """Format an OpInfo name for display, adding aten. prefix for simple names."""
    if "." not in opinfo_name:
        return f"aten.{opinfo_name}"
    return opinfo_name

