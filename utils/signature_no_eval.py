
def signature_no_eval(f: Callable[..., Any]) -> Signature:
    """Get the signature of a callable without evaluating any annotations."""
    if sys.version_info >= (3, 14):
        from annotationlib import Format

        return signature(f, annotation_format=Format.FORWARDREF)
    else:
        return signature(f)

