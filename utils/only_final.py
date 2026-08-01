
def only_final() -> Option:
    release_control = ReleaseControl(set(), set())
    return Option(
        "--only-final",
        dest="release_control",
        action="callback",
        callback=_handle_only_final,
        type="str",
        default=release_control,
        help="Only allow final releases (no pre-releases) for a package. Can be "
        "supplied multiple times, and each time adds to the existing value. "
        'Accepts either ":all:" to disable pre-releases for all packages, '
        '":none:" to empty the set, or one or more package names with commas '
        "between them. Cannot be used with --pre.",
    )

