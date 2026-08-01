
def get_size_dict(
    size: int | Iterable[int] | dict[str, int] | SizeDict | None = None,
    max_size: int | None = None,
    height_width_order: bool = True,
    default_to_square: bool = True,
    param_name="size",
) -> dict:
    """
    Converts the old size parameter in the config into the new dict expected in the config. This is to ensure backwards
    compatibility with the old image processor configs and removes ambiguity over whether the tuple is in (height,
    width) or (width, height) format.

    - If `size` is tuple, it is converted to `{"height": size[0], "width": size[1]}` or `{"height": size[1], "width":
    size[0]}` if `height_width_order` is `False`.
    - If `size` is an int, and `default_to_square` is `True`, it is converted to `{"height": size, "width": size}`.
    - If `size` is an int and `default_to_square` is False, it is converted to `{"shortest_edge": size}`. If `max_size`
      is set, it is added to the dict as `{"longest_edge": max_size}`.
    - If `size` is `None` and `default_to_square` is False, the result is `{"longest_edge": max_size}` (requires
      `max_size` to be set). Tuple/list/SizeDict/dict `size` values do not use `max_size`.

    Args:
        size (`int | Iterable[int] | dict[str, int] | SizeDict`, *optional*):
            The `size` parameter to be cast into a size dictionary.
        max_size (`int | None`, *optional*):
            With `default_to_square=False`, sets `longest_edge` when `size` is an int or `None`; unused for dict,
            `SizeDict`, or tuple/list `size`. Raises if set with `default_to_square=True` when `size` is an int or `None`.
        height_width_order (`bool`, *optional*, defaults to `True`):
            If `size` is a tuple, whether it's in (height, width) or (width, height) order.
        default_to_square (`bool`, *optional*, defaults to `True`):
            If `size` is an int, whether to default to a square image or not.
    """
    if not isinstance(size, dict | SizeDict):
        size_dict = convert_to_size_dict(size, max_size, default_to_square, height_width_order)
        logger.info(
            f"{param_name} should be a dictionary with one of the following sets of keys: {VALID_SIZE_DICT_KEYS}, got {size}."
            f" Converted to {size_dict}.",
        )
    # Some remote code bypasses or overrides `_standardize_kwargs`, so handle `SizeDict` `size` here too.
    elif isinstance(size, SizeDict):
        size_dict = dict(size)
    else:
        size_dict = size

    if not is_valid_size_dict(size_dict):
        raise ValueError(
            f"{param_name} must have one of the following set of keys: {VALID_SIZE_DICT_KEYS}, got {size_dict.keys()}"
        )
    return size_dict

