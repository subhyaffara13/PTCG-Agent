
def requirements() -> Option:
    return Option(
        "-r",
        "--requirement",
        # See https://github.com/di/pip-api/commit/7e2f1e8693da249156b99ec593af1e61192c611a#r64188234
        # --requirements is not a valid pip option
        # but we accept anyway as it may exist in the wild
        "--requirements",
        dest="requirements",
        action="append",
        default=[],
        metavar="file",
        help="Install from the given requirements file. "
        "This option can be used multiple times.",
    )


def requirements() -> Option:
    return Option(
        "-r",
        "--requirement",
        dest="requirements",
        action="append",
        default=[],
        metavar="file",
        help=(
            "Install from the given requirements file. "
            "The file or URL can be in pip's requirements.txt format, "
            "or pylock.toml format. pylock.toml support is experimental. "
            "This option can be used multiple times."
        ),
    )

