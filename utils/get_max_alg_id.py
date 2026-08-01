
def get_max_alg_id() -> int | None:
    if not _init():
        return None
    return __MAX_ALG_ID

