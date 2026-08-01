
def _class_name(nodeid: str) -> str | None:
    parts = nodeid.split("::")
    # nodeid can be: file::Class::test or file::test
    if len(parts) >= 3:
        return parts[-2]
    return None

