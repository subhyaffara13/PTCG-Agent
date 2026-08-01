
def _handle_only_final(
    option: Option, opt_str: str, value: str, parser: OptionParser
) -> None:
    existing = _get_release_control(parser.values, option)
    existing.handle_mutual_excludes(
        value,
        existing.only_final,
        existing.all_releases,
        "only_final",
    )

