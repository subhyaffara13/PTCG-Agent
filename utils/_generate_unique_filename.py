
def _generate_unique_filename(cls: type, func_name: str) -> str:
    """
    Create a "filename" suitable for a function being generated.
    """
    return (
        f"<attrs generated {func_name} {cls.__module__}."
        f"{getattr(cls, '__qualname__', cls.__name__)}>"
    )

