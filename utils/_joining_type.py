
def _joining_type(cp: int) -> Optional[str]:
    for jt, ranges in idnadata.joining_types.items():
        if intranges_contain(cp, ranges):
            return jt
    return None

