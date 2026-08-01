
def _prepare_attribute_parts(
    attr: t.Optional[t.Union[str, int]],
) -> t.List[t.Union[str, int]]:
    if attr is None:
        return []

    if isinstance(attr, str):
        return [int(x) if x.isdigit() else x for x in attr.split(".")]

    return [attr]

