
def cmdoptions_hash() -> Option:
    return Option(
        "--hash",
        dest="hashes",
        action="append",
        default=[],
        help="Verify that the package's archive matches this "
        "hash before installing. Example: --hash=sha256:abcdef...",
    )

