
def all_releases() -> Option:
    release_control = ReleaseControl(set(), set())
    return Option(
        "--all-releases",
        dest="release_control",
        action="callback",
        callback=_handle_all_releases,
        type="str",
        default=release_control,
        help="Allow all release types (including pre-releases) for a package. "
        "Can be supplied multiple times, and each time adds to the existing "
        'value. Accepts either ":all:" to allow pre-releases for all '
        'packages, ":none:" to empty the set (notice the colons), or one or '
        "more package names with commas between them (no colons). Cannot be "
        "used with --pre.",
    )

