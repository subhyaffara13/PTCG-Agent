
def _parse_format_value(value: str) -> "OutputFormat":
    try:
        return OutputFormat(value)
    except ValueError:
        valid = ", ".join(m.value for m in OutputFormat)
        raise click.UsageError(f"Invalid value for '--format': '{value}'. Valid values: {valid}.") from None

