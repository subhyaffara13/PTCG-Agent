
def get_lexer_for_response(response: Response) -> str:
    content_type = response.headers.get("Content-Type")
    if content_type is not None:
        mime_type, _, _ = content_type.partition(";")
        try:
            return typing.cast(
                str, pygments.lexers.get_lexer_for_mimetype(mime_type.strip()).name
            )
        except pygments.util.ClassNotFound:  # pragma: no cover
            pass
    return ""  # pragma: no cover

