
def truncation_validator(value: bool | str | TruncationStrategy | None = None):
    possible_names = ["only_first", "only_second", "longest_first", "do_not_truncate"]
    if value is None:
        pass
    elif not isinstance(value, (bool, str, TruncationStrategy)):
        raise ValueError("Value for truncation must be either a boolean, a string or a `TruncationStrategy`")
    elif isinstance(value, str) and value not in possible_names:
        raise ValueError(f"If truncation is a string, value must be one of {possible_names}")

