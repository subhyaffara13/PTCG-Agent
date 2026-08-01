
def highest_version(versions: list[str]) -> str:
    return max(versions, key=parse_version)

