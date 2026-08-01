
def allow_external() -> Option:
    return Option(
        "--allow-external",
        dest="allow_external",
        action="append",
        default=[],
    )

