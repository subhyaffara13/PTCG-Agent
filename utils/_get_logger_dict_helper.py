
def _get_logger_dict_helper(
    mod: nn.Module,
    target_dict: dict[str, Any],
    prefix: str = "",
) -> None:
    r"""This is the helper function for get_logger_dict

    Args:
        mod: module we want to save all logger stats
        prefix: prefix for the current module
        target_dict: the dictionary used to save all logger stats
    """

    def get_prefix(prefix):
        return prefix if prefix == "" else prefix + "."

    for child in mod.children():
        if isinstance(child, Logger):
            target_dict[get_prefix(prefix) + "stats"] = child.stats
            break

    for name, child in mod.named_children():
        module_prefix = get_prefix(prefix) + name if prefix else name
        _get_logger_dict_helper(child, target_dict, module_prefix)

