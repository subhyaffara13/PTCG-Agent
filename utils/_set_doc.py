
def _set_doc(obj):
    if obj.__doc__:
        obj.__doc__ = obj.__doc__ % _doc_parts

