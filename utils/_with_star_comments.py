
def _with_star_comments(parsed: parse.ParsedContent, module: str, comments: list[str]) -> list[str]:
    star_comment = parsed.categorized_comments["nested"].get(module, {}).pop("*", None)
    if star_comment:
        return [*comments, star_comment]
    return comments

