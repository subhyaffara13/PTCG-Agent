
def try_split(v: str | Sequence[str] | object, split_regex: str = ",") -> list[str]:
    """Split and trim a str or sequence (eg: list) of str into a list of str.
    If an element of the input is not str, a type error will be raised."""

    def complain(x: object, additional_info: str = "") -> Never:
        raise argparse.ArgumentTypeError(
            f"Expected a list or a stringified version thereof, but got: '{x}', of type {type(x).__name__}.{additional_info}"
        )

    if isinstance(v, str):
        items = [p.strip() for p in re.split(split_regex, v)]
        if items and items[-1] == "":
            items.pop(-1)
        return items
    elif isinstance(v, Sequence):
        return [
            (
                p.strip()
                if isinstance(p, str)
                else complain(p, additional_info=" (As an element of the list.)")
            )
            for p in v
        ]
    else:
        complain(v)

