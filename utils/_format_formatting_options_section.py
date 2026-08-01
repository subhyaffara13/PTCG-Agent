
def _format_formatting_options_section(formatter: click.HelpFormatter) -> None:
    with formatter.section("Formatting options"):
        formatter.write_dl(_FORMATTING_OPTIONS_HELP_RECORDS)

