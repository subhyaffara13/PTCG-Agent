
def _detect_discard_mscu(select, sel_type):
    if sel_type not in (1, 2, 4): return False
    if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"): return True
    return False


def _detect_discard_mscu(select, sel_type):
    if sel_type not in (1, 2, 4): return False
    if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"): return True
    return False

