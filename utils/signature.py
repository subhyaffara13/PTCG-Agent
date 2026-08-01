
def signature(obj: Callable[..., Any]) -> Signature:
    """Return signature without evaluating annotations."""
    if sys.version_info >= (3, 14):
        return inspect.signature(obj, annotation_format=Format.STRING)
    return inspect.signature(obj)


def signature(
    f: NativeFunction, *, method: bool = False, pyi: bool = False
) -> PythonSignature:
    return signature_from_schema(
        f.func, category_override=f.category_override, method=method, pyi=pyi
    )

