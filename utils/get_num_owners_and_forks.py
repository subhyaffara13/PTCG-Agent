
def get_num_owners_and_forks() -> tuple[str, str]:
    """
    Retrieves number of OwnerRRefs and forks on this node from
    _rref_context_get_debug_info.
    """
    rref_dbg_info = _rref_context_get_debug_info()
    num_owners = rref_dbg_info["num_owner_rrefs"]
    num_forks = rref_dbg_info["num_forks"]
    return num_owners, num_forks

