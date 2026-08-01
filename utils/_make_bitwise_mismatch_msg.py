
def _make_bitwise_mismatch_msg(
    *,
    default_identifier: str,
    identifier: str | Callable[[str], str] | None = None,
    extra: str | None = None,
    first_mismatch_idx: tuple[int, ...] | None = None,
):
    """Makes a mismatch error message for bitwise values.

    Args:
        default_identifier (str): Default description of the compared values, e.g. "Tensor-likes".
        identifier (Optional[Union[str, Callable[[str], str]]]): Optional identifier that overrides
            ``default_identifier``. Can be passed as callable in which case it will be called with
            ``default_identifier`` to create the description at runtime.
        extra (Optional[str]): Extra information to be placed after the message header and the mismatch statistics.
        first_mismatch_idx (Optional[tuple[int, ...]]): the index of the first mismatch, for each dimension.
    """
    if identifier is None:
        identifier = default_identifier
    elif callable(identifier):
        identifier = identifier(default_identifier)

    msg = f"{identifier} are not 'equal'!\n\n"

    if extra:
        msg += f"{extra.strip()}\n"
    if first_mismatch_idx is not None:
        msg += f"The first mismatched element is at index {first_mismatch_idx}.\n"
    return msg.strip()

