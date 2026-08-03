import re

def remove_misplaced_type_comments(source: bytes) -> bytes: ...


def remove_misplaced_type_comments(source: str) -> str: ...


def remove_misplaced_type_comments(source: str | bytes) -> str | bytes:
    """Remove comments from source that could be understood as misplaced type comments.

    Normal comments may look like misplaced type comments, and since they cause blocking
    parse errors, we want to avoid them.
    """
    if isinstance(source, bytes):
        # This gives us a 1-1 character code mapping, so it's roundtrippable.
        text = source.decode("latin1")
    else:
        text = source

    # Remove something that looks like a variable type comment but that's by itself
    # on a line, as it will often generate a parse error (unless it's # type: ignore).
    text = re.sub(r'^[ \t]*# +type: +["\'a-zA-Z_].*$', "", text, flags=re.MULTILINE)

    # Remove something that looks like a function type comment after docstring,
    # which will result in a parse error.
    text = re.sub(r'""" *\n[ \t\n]*# +type: +\(.*$', '"""\n', text, flags=re.MULTILINE)
    text = re.sub(r"''' *\n[ \t\n]*# +type: +\(.*$", "'''\n", text, flags=re.MULTILINE)

    # Remove something that looks like a badly formed function type comment.
    text = re.sub(r"^[ \t]*# +type: +\([^()]+(\)[ \t]*)?$", "", text, flags=re.MULTILINE)

    if isinstance(source, bytes):
        return text.encode("latin1")
    else:
        return text

