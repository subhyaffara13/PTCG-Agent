
def ast3_parse(
    source: str | bytes, filename: str, mode: str, feature_version: int = PY_MINOR_VERSION
) -> AST:
    # Ignore warnings that look like:
    #     <type_comment>:1: SyntaxWarning: invalid escape sequence '\.'
    # because `source` could be anything, including literals like r'(re\.match)'
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return ast3.parse(
            source,
            filename,
            mode,
            type_comments=True,  # This works the magic
            feature_version=feature_version,
        )

