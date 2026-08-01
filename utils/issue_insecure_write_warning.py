
def issue_insecure_write_warning() -> None:
    """Issue an insecure write warning."""

    def format_warning(msg: str, *args: Any, **kwargs: Any) -> str:  # noqa: ARG001
        return str(msg) + "\n"

    warnings.formatwarning = format_warning  # type:ignore[assignment]
    warnings.warn(
        "WARNING: Insecure writes have been enabled via environment variable "
        "'JUPYTER_ALLOW_INSECURE_WRITES'! If this is not intended, remove the "
        "variable or set its value to 'False'.",
        stacklevel=2,
    )

