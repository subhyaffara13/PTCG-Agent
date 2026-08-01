
def add_region_and_context_region(
    physical_location, line_range, col_offset, end_col_offset, code
):
    if code:
        first_line_number, snippet_lines = parse_code(code)
        snippet_line = snippet_lines[line_range[0] - first_line_number]
        snippet = om.ArtifactContent(text=snippet_line)
    else:
        snippet = None

    physical_location.region = om.Region(
        start_line=line_range[0],
        end_line=line_range[1] if len(line_range) > 1 else line_range[0],
        start_column=col_offset + 1,
        end_column=end_col_offset + 1,
        snippet=snippet,
    )

    if code:
        physical_location.context_region = om.Region(
            start_line=first_line_number,
            end_line=first_line_number + len(snippet_lines) - 1,
            snippet=om.ArtifactContent(text="".join(snippet_lines)),
        )

