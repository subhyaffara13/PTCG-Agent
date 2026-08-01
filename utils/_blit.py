
def _blit(argsid):
    """
    Thin wrapper to blit called via tkapp.call.

    *argsid* is a unique string identifier to fetch the correct arguments from
    the ``_blit_args`` dict, since arguments cannot be passed directly.
    """
    photoimage, data, offsets, bbox, comp_rule = _blit_args.pop(argsid)
    if not photoimage.tk.call("info", "commands", photoimage):
        return
    _tkagg.blit(photoimage.tk.interpaddr(), str(photoimage), data, comp_rule, offsets,
                bbox)

