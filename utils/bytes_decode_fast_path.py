
def bytes_decode_fast_path(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    """Specialize common cases of obj.decode for most used encodings and strict errors."""

    if not isinstance(callee, MemberExpr):
        return None

    # We can only specialize if we have string literals as args
    if len(expr.arg_kinds) > 0 and not isinstance(expr.args[0], StrExpr):
        return None
    if len(expr.arg_kinds) > 1 and not isinstance(expr.args[1], StrExpr):
        return None

    encoding = "utf8"
    errors = "strict"
    if len(expr.arg_kinds) > 0 and isinstance(expr.args[0], StrExpr):
        if expr.arg_kinds[0] == ARG_NAMED:
            if expr.arg_names[0] == "encoding":
                encoding = expr.args[0].value
            elif expr.arg_names[0] == "errors":
                errors = expr.args[0].value
        elif expr.arg_kinds[0] == ARG_POS:
            encoding = expr.args[0].value
        else:
            return None
    if len(expr.arg_kinds) > 1 and isinstance(expr.args[1], StrExpr):
        if expr.arg_kinds[1] == ARG_NAMED:
            if expr.arg_names[1] == "encoding":
                encoding = expr.args[1].value
            elif expr.arg_names[1] == "errors":
                errors = expr.args[1].value
        elif expr.arg_kinds[1] == ARG_POS:
            errors = expr.args[1].value
        else:
            return None

    if errors != "strict":
        # We can only specialize strict errors
        return None

    encoding = encoding.lower().replace("_", "-")  # normalize
    # Specialized encodings and their accepted aliases
    if encoding in ["u8", "utf", "utf8", "utf-8", "cp65001"]:
        return builder.call_c(bytes_decode_utf8_strict, [builder.accept(callee.expr)], expr.line)
    elif encoding in ["646", "ascii", "usascii", "us-ascii"]:
        return builder.call_c(bytes_decode_ascii_strict, [builder.accept(callee.expr)], expr.line)
    elif encoding in [
        "iso8859-1",
        "iso-8859-1",
        "8859",
        "cp819",
        "latin",
        "latin1",
        "latin-1",
        "l1",
    ]:
        return builder.call_c(bytes_decode_latin1_strict, [builder.accept(callee.expr)], expr.line)

    return None

