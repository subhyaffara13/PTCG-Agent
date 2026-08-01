
def _flake8_normalize(
    value: str,
    *args: str,
    comma_separated_list: bool = False,
    normalize_paths: bool = False,
) -> str | list[str]:
    ret: str | list[str] = value
    if comma_separated_list and isinstance(ret, str):
        ret = utils.parse_comma_separated_list(value)

    if normalize_paths:
        if isinstance(ret, str):
            ret = utils.normalize_path(ret, *args)
        else:
            ret = utils.normalize_paths(ret, *args)

    return ret

