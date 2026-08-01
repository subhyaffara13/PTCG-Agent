
def safe_get_annotations(obj: Any) -> dict[str, Any]:
    """Get the annotations for the provided object, accounting for potential deferred forward references.

    Starting with Python 3.14, accessing the `__annotations__` attribute might raise a `NameError` if
    a referenced symbol isn't defined yet. In this case, we return the annotation in the *forward ref*
    format.
    """
    if sys.version_info >= (3, 14):
        return annotationlib.get_annotations(obj, format=annotationlib.Format.FORWARDREF)
    else:
        # TODO just do getattr(obj, '__annotations__', {}) when dropping support for Python 3.9:
        if isinstance(obj, type):
            return obj.__dict__.get('__annotations__', {})
        else:
            return getattr(obj, '__annotations__', {})

