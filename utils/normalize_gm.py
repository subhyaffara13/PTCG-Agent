
def normalize_gm(gm_str: str) -> str:
    # strip comments as comments have path to files which may differ from
    # system to system.
    stripped = strip_comment(gm_str)
    no_trailing = remove_trailing_space(stripped)
    return _squash_blank_lines(no_trailing)

