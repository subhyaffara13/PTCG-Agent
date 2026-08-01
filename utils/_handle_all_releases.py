
def _handle_all_releases(
    option: Option, opt_str: str, value: str, parser: OptionParser
) -> None:
    existing = _get_release_control(parser.values, option)
    existing.handle_mutual_excludes(
        value,
        existing.all_releases,
        existing.only_final,
        "all_releases",
    )

