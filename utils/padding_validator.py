
def padding_validator(value: bool | str | PaddingStrategy | None = None):
    possible_names = ["longest", "max_length", "do_not_pad"]
    if value is None:
        pass
    elif not isinstance(value, (bool, str, PaddingStrategy)):
        raise ValueError("Value for padding must be either a boolean, a string or a `PaddingStrategy`")
    elif isinstance(value, str) and value not in possible_names:
        raise ValueError(f"If padding is a string, the value must be one of {possible_names}")

