
def allow_unverified() -> Option:
    return Option(
        "--allow-unverified",
        dest="allow_unverified",
        action="append",
        default=[],
    )

