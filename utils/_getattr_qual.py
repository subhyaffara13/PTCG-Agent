
def _getattr_qual(obj, name, default=_NOTHING):
    try:
        for path in name.split("."):
            obj = getattr(obj, path)
        return obj
    except AttributeError:
        if default is not _NOTHING:
            return default
        else:
            raise

