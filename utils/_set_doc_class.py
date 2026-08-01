
def _set_doc_class(obj):
    if obj.__doc__:
        doc_parts = _doc_parts.copy()
        doc_parts["params_basic"] = ""
        doc_parts["params_extra"] = ""
        obj.__doc__ = obj.__doc__ % doc_parts

