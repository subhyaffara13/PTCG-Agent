
def _named_parameters_with_duplicates(
    module: nn.Module, **kwargs: Any
) -> list[tuple[str, nn.Parameter]]:
    """
    This API is required as some modules overwrite `named_parameters()` but do not support
    `remove_duplicate`.
    """
    if "remove_duplicate" in kwargs:
        raise AssertionError(
            "_named_parameters_with_duplicates cannot be used with `remove_duplicate` argument."
        )
    kwargs["remove_duplicate"] = False
    try:
        ret = list(module.named_parameters(**kwargs))
    except AssertionError:
        kwargs.pop("remove_duplicate")
        ret = list(module.named_parameters(**kwargs))
    return ret

