import functools

def _compat_get_offset(meth):
    """
    Decorator for the get_offset method of OffsetBox and subclasses, that
    allows supporting both the new signature (self, bbox, renderer) and the old
    signature (self, width, height, xdescent, ydescent, renderer).
    """
    sigs = [lambda self, width, height, xdescent, ydescent, renderer: locals(),
            lambda self, bbox, renderer: locals()]

    @functools.wraps(meth)
    def get_offset(self, *args, **kwargs):
        params = _api.select_matching_signature(sigs, self, *args, **kwargs)
        bbox = (params["bbox"] if "bbox" in params else
                Bbox.from_bounds(-params["xdescent"], -params["ydescent"],
                                 params["width"], params["height"]))
        return meth(params["self"], bbox, params["renderer"])
    return get_offset

