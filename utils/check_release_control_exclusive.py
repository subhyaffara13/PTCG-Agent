
def check_release_control_exclusive(options: Values) -> None:
    """
    Raise an error if --pre is used with --all-releases or --only-final,
    and transform --pre into --all-releases :all: if used alone.
    """
    if not hasattr(options, "pre") or not options.pre:
        return

    release_control = options.release_control
    if release_control.all_releases or release_control.only_final:
        raise CommandError("--pre cannot be used with --all-releases or --only-final.")

    # Transform --pre into --all-releases :all:
    release_control.all_releases.add(":all:")

