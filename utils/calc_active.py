
def calc_active(seg):
    return sum(b["size"] for b in seg["blocks"] if b["state"] == "active_allocated")

