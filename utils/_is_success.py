
def _is_success(*statuslist: PropagateStatus) -> bool:
    return not any(status == PropagateStatus.FAIL for status in statuslist)

