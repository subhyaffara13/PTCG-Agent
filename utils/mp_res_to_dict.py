
def mp_res_to_dict(mp_result):
    """Formats an MPResult namedtuple into a dict for JSON dumping"""
    return {
        "src_case": to_dict(mp_result.src_case),

        # np assert can't handle mpf, so take the accuracy hit here.
        "mp_result": float(mp_result.mp_result)
    }

