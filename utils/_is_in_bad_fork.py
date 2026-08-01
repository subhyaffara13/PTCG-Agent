
def _is_in_bad_fork() -> bool:
    return torch._C._mtia_isInBadFork()

