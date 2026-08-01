
def _unpack_zerodim_and_defer(method: F, name: str) -> F:
    """
    Boilerplate for pandas conventions in arithmetic and comparison methods.

    Ensure method returns NotImplemented when operating against "senior"
    classes.  Ensure zero-dimensional ndarrays are always unpacked.

    Parameters
    ----------
    method : binary method
    name : str

    Returns
    -------
    method
    """
    is_logical = name.strip("_") in ["or", "xor", "and", "ror", "rxor", "rand"]

    @wraps(method)
    def new_method(self, other):
        prio = getattr(other, "__pandas_priority__", None)
        if prio is not None:
            if prio > self.__pandas_priority__:
                # e.g. other is DataFrame while self is Index/Series/EA
                return NotImplemented

        other = item_from_zerodim(other)
        if (
            isinstance(self, ABCExtensionArray)
            and isinstance(other, list)
            and not is_logical
        ):
            # See GH#62423
            other = sanitize_array(other, None)
            other = ensure_wrapped_if_datetimelike(other)

        return method(self, other)

    # error: Incompatible return value type (got "Callable[[Any, Any], Any]",
    # expected "F")
    return new_method  # type: ignore[return-value]

