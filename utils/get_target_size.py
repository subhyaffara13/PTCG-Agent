
def get_target_size(size_dict: dict[str, int]) -> tuple[int, int]:
    """Returns the height and width from a size dict."""
    target_height = size_dict["shortest_edge"]
    target_width = size_dict["longest_edge"] or target_height

    return target_height, target_width


def get_target_size(size_dict: dict[str, int]) -> tuple[int, int]:
    """Returns the height and width from a size dict."""
    target_height = size_dict["shortest_edge"]
    target_width = size_dict["longest_edge"] or target_height

    return target_height, target_width

