
def _add_docstring(obj, doc, warn_on_python):
    if warn_on_python and not _needs_add_docstring(obj):
        warnings.warn(
            f"add_newdoc was used on a pure-python object {obj}. "
            "Prefer to attach it directly to the source.",
            UserWarning,
            stacklevel=3)

    doc = inspect.cleandoc(doc)

    try:
        add_docstring(obj, doc)
    except Exception:
        pass

