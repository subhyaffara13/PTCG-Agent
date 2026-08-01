
def get_submod_name(stage_idx: int):
    """Returns the name of the submod for a given stage index.
    For example, "submod_pp_0", "submod_pp_1", etc.
    """
    return "_".join([PP_SUBMOD_PREFIX, str(stage_idx)])

