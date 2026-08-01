
def add_hop_context(cls: type[HOP_VT_Alias]) -> type[HOP_VT_Alias]:
    """
    Class decorator that adds HOP context to exceptions raised in call_function.

    Requires the class to have _HOP_NAME and _ALLOW_FALLBACK_TO_EAGER set.
    """

    if hasattr(cls.call_method, "_hop_wrapped"):
        return cls

    if cls._HOP_NAME is None:
        raise TypeError(f"{cls.__name__} must define _HOP_NAME class attribute.")
    if cls._ALLOW_FALLBACK_TO_EAGER is None:
        raise TypeError(
            f"{cls.__name__} must define _ALLOW_FALLBACK_TO_EAGER class attribute."
        )

    original_call_function = cls.call_function

    @functools.wraps(original_call_function)
    def wrapped_call_function(self, *args: Any, **kwargs: Any) -> VariableTracker:
        try:
            return original_call_function(self, *args, **kwargs)
        except UncapturedHigherOrderOpError as e:
            if not hasattr(e, "_hop_name"):
                e._hop_name = self._HOP_NAME  # pyrefly: ignore[missing-attribute]
            raise
        except (Unsupported, ObservedException) as e:
            # Only tag if not already tagged (reports deepest HOP only)
            if hasattr(e, "_hop_name"):
                raise

            if self._ALLOW_FALLBACK_TO_EAGER:
                # Tag the exception with HOP name for later formatting in exc.py
                # NOTE: because nested graph breaks are NOT supported on HOPs, we will
                # NEVER log a HOP graph break before running this
                e._hop_name = self._HOP_NAME  # pyrefly: ignore[missing-attribute]
                raise
            else:
                real_stack = getattr(e, "real_stack", None)
                full_msg = (
                    "This higher order operator doesn't work unless it is "
                    "captured completely with torch.compile. Got graph break/error:"
                    f"\n\n{str(e)}"
                )
                exc = UncapturedHigherOrderOpError(full_msg, real_stack)
                exc._hop_name = self._HOP_NAME  # pyrefly: ignore[missing-attribute]
                raise exc.with_traceback(e.__traceback__) from None

    wrapped_call_function._hop_wrapped = True  # pyrefly: ignore[missing-attribute]
    cls.call_function = wrapped_call_function
    return cls

