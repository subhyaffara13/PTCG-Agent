
def _block_extra_legacy(b):
    if "history" in b:
        frames = b["history"][0].get("frames", [])
        real_size = b["history"][0]["real_size"]
    else:
        real_size = b.get("requested_size", b["size"])
        frames = []
    return frames, real_size

