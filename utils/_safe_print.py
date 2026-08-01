
def _safe_print(s):
    encoding = getattr(sys.stdout, 'encoding', None)
    if encoding is not None:
        s = s.encode(encoding, 'backslashreplace').decode(encoding)
    print(s, end=' ')


def _safe_print(*args: Any, **kwargs: Any) -> None:
    """Safe print that avoids recursive torch function dispatches."""
    import sys

    # Convert any torch objects to basic representations
    safe_args = []
    for arg in args:
        if hasattr(arg, "__class__") and "torch" in str(type(arg)):
            safe_args.append(f"<{type(arg).__name__}>")
        else:
            safe_args.append(str(arg))

    print(*safe_args, **kwargs, file=sys.stderr)

