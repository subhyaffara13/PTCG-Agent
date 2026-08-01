
def _create_tag_line_pattern(inner_pattern, ignore_case=False):
    return ((r"(?i)" if ignore_case else r"")
        + r"^(##)( *)"  # groups 1, 2
        + inner_pattern  # group 3
        + r"( *)(:)( *)(.*?)( *)$")  # groups 4, 5, 6, 7, 8

