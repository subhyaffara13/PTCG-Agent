
def _create_tag_line_token(inner_pattern, inner_token, ignore_case=False):
    # this function template-izes the tag line for a specific type of tag, which will
    # have a different pattern and different token. otherwise, everything about a tag
    # line is the same
    return (
        _create_tag_line_pattern(inner_pattern, ignore_case=ignore_case),
        bygroups(
            Keyword.Declaration,
            Text.Whitespace,
            inner_token,
            Text.Whitespace,
            Punctuation,
            Text.Whitespace,
            String,
            Text.Whitespace,
        ),
    )

