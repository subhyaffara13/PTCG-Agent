
def _format_epilog_no_indent(epilog: str | None, ctx: click.Context, formatter: click.HelpFormatter) -> None:
    """Write the epilog without indentation."""
    if epilog:
        formatter.write_paragraph()
        for line in epilog.split("\n"):
            formatter.write_text(line)

