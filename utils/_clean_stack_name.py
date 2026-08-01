
def _clean_stack_name(stack_name: str) -> str:
    """
    Clean up FX node's nn_module_stack metadata string to match the module name hierarchies

    Example:
        Input: "L['self']._modules['layers']['0']._modules['attention']"
        Output: "layers.0.attention"
    """
    cleaned = re.sub(r"^L\['self'\]\.?", "", stack_name)
    parts = re.findall(r"\['([^']+)'\]", cleaned)
    return ".".join(parts) if parts else cleaned

