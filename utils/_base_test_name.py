
def _base_test_name(nodeid: str) -> str:
    # Strip parameters like [param=..] from the last component
    name = nodeid.split("::")[-1]
    return re.sub(r"\[.*\]$", "", name)

