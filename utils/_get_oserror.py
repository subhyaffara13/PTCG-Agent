
def _get_oserror(error: int, *, encoder: bool) -> OSError:
    try:
        msg = Image.core.getcodecstatus(error)
    except AttributeError:
        msg = ERRORS.get(error)
    if not msg:
        msg = f"{'encoder' if encoder else 'decoder'} error {error}"
    msg += f" when {'writing' if encoder else 'reading'} image file"
    return OSError(msg)

