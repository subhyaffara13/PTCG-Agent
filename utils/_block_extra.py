
def _block_extra(b):
    if "frames" not in b:
        # old snapshot format made it more complicated to get frames/allocated size
        return _block_extra_legacy(b)
    return b["frames"], b["requested_size"]

