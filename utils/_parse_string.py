
def _parse_string(
    data: str, type_comments: bool = True, modname: str | None = None
) -> tuple[ast.Module, ParserModule]:
    parser_module = get_parser_module(type_comments=type_comments)
    try:
        parsed = parser_module.parse(
            data + "\n", type_comments=type_comments, filename=modname
        )
    except SyntaxError as exc:
        # If the type annotations are misplaced for some reason, we do not want
        # to fail the entire parsing of the file, so we need to retry the
        # parsing without type comment support. We use a heuristic for
        # determining if the error is due to type annotations.
        type_annot_related = re.search(r"#\s+type:", exc.text or "")
        if not (type_annot_related and type_comments):
            raise

        parser_module = get_parser_module(type_comments=False)
        parsed = parser_module.parse(data + "\n", type_comments=False)
    return parsed, parser_module

