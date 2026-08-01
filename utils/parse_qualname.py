
def parse_qualname(qualname: str) -> tuple[str, str]:
    names = qualname.split("::", 1)
    if len(names) != 2:
        raise ValueError(
            f"Expected there to be a namespace in {qualname}, i.e. The "
            f"operator name should look something like ns::foo"
        )
    if "." in names[1]:
        raise ValueError(
            f"The torch.custom_ops APIs do not handle overloads, "
            f"i.e. operator names with '.' in them. "
            f"Please name your operator something like ns::foo. "
            f"Got: {qualname}"
        )
    return names[0], names[1]

