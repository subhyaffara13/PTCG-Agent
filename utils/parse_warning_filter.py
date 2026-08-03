import re

def parse_warning_filter(
    arg: str, *, escape: bool
) -> tuple[warnings._ActionKind, str, type[Warning], str, int]:
    """Parse a warnings filter string.

    This is copied from warnings._setoption with the following changes:

    * Does not apply the filter.
    * Escaping is optional.
    * Raises UsageError so we get nice error messages on failure.
    """
    __tracebackhide__ = True
    error_template = dedent(
        f"""\
        while parsing the following warning configuration:

          {arg}

        This error occurred:

        {{error}}
        """
    )

    parts = arg.split(":")
    if len(parts) > 5:
        doc_url = (
            "https://docs.python.org/3/library/warnings.html#describing-warning-filters"
        )
        error = dedent(
            f"""\
            Too many fields ({len(parts)}), expected at most 5 separated by colons:

              action:message:category:module:line

            For more information please consult: {doc_url}
            """
        )
        raise UsageError(error_template.format(error=error))

    while len(parts) < 5:
        parts.append("")
    action_, message, category_, module, lineno_ = (s.strip() for s in parts)
    try:
        action: warnings._ActionKind = warnings._getaction(action_)  # type: ignore[attr-defined]
    except warnings._OptionError as e:
        raise UsageError(error_template.format(error=str(e))) from None
    try:
        category: type[Warning] = _resolve_warning_category(category_)
    except ImportError:
        raise
    except Exception:
        exc_info = ExceptionInfo.from_current()
        exception_text = exc_info.getrepr(style="native")
        raise UsageError(error_template.format(error=exception_text)) from None
    if message and escape:
        message = re.escape(message)
    if module and escape:
        module = re.escape(module) + r"\Z"
    if lineno_:
        try:
            lineno = int(lineno_)
            if lineno < 0:
                raise ValueError("number is negative")
        except ValueError as e:
            raise UsageError(
                error_template.format(error=f"invalid lineno {lineno_!r}: {e}")
            ) from None
    else:
        lineno = 0
    try:
        re.compile(message)
        re.compile(module)
    except re.error as e:
        raise UsageError(
            error_template.format(error=f"Invalid regex {e.pattern!r}: {e}")
        ) from None
    return action, message, category, module, lineno

