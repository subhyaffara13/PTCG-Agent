
def _format_glyph_errors(errors: Mapping[str, Exception]) -> str:
    lines = []
    for baseGlyph, error in sorted(errors.items()):
        lines.append(f"    {baseGlyph} => {type(error).__name__}: {error}")
    return "\n".join(lines)

