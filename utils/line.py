
def line(content: str, line_separator: str, config: Config = DEFAULT_CONFIG) -> str:
    """Returns a line wrapped to the specified line-length, if possible."""
    wrap_mode = config.multi_line_output
    if len(content) > config.line_length and wrap_mode != Modes.NOQA:  # type: ignore
        line_without_comment = content
        comment = None
        if "#" in content:
            line_without_comment, comment = content.split("#", 1)
        for splitter in ("import ", "cimport ", ".", "as "):
            exp = r"\b" + re.escape(splitter) + r"\b"
            if re.search(exp, line_without_comment) and not line_without_comment.strip().startswith(
                splitter
            ):
                line_parts = re.split(exp, line_without_comment)
                if comment and not (config.use_parentheses and "noqa" in comment):
                    _comma_maybe = (
                        ","
                        if (
                            config.include_trailing_comma
                            and config.use_parentheses
                            and not line_without_comment.rstrip().endswith(",")
                        )
                        else ""
                    )
                    line_parts[-1] = (
                        f"{line_parts[-1].strip()}{_comma_maybe}{config.comment_prefix}{comment}"
                    )
                next_line = []
                while (len(content) + 2) > (
                    config.wrap_length or config.line_length
                ) and line_parts:
                    next_line.append(line_parts.pop())
                    content = splitter.join(line_parts)
                if not content:
                    content = next_line.pop()

                cont_line = _wrap_line(
                    config.indent + splitter.join(next_line).lstrip(),
                    line_separator,
                    config,
                )
                if config.use_parentheses:
                    if splitter == "as ":
                        output = f"{content}{splitter}{cont_line.lstrip()}"
                    else:
                        _comma = "," if config.include_trailing_comma and not comment else ""

                        if wrap_mode in (
                            Modes.VERTICAL_HANGING_INDENT,  # type: ignore
                            Modes.VERTICAL_GRID_GROUPED,  # type: ignore
                        ):
                            _separator = line_separator
                        else:
                            _separator = ""
                        noqa_comment = ""
                        if comment and "noqa" in comment:
                            noqa_comment = f"{config.comment_prefix}{comment}"
                            cont_line = cont_line.rstrip()
                            _comma = "," if config.include_trailing_comma else ""
                        output = (
                            f"{content}{splitter}({noqa_comment}"
                            f"{line_separator}{cont_line}{_comma}{_separator})"
                        )
                        lines = output.split(line_separator)
                        if config.comment_prefix in lines[-1] and lines[-1].endswith(")"):
                            content, comment = lines[-1].split(config.comment_prefix, 1)
                            lines[-1] = content + ")" + config.comment_prefix + comment[:-1]
                        output = line_separator.join(lines)
                    return output
                return f"{content}{splitter}\\{line_separator}{cont_line}"
    elif len(content) > config.line_length and wrap_mode == Modes.NOQA and "# NOQA" not in content:  # type: ignore
        return f"{content}{config.comment_prefix} NOQA"

    return content


def line(loc: int, strg: str) -> str:
    """
    Returns the line of text containing loc within a string, counting newlines as line separators.
    """
    last_cr = strg.rfind("\n", 0, loc)
    next_cr = strg.find("\n", loc)
    return strg[last_cr + 1 : next_cr] if next_cr >= 0 else strg[last_cr + 1 :]


def line(loc, strg):
    """Returns the line of text containing loc within a string, counting newlines as line separators.
       """
    lastCR = strg.rfind("\n", 0, loc)
    nextCR = strg.find("\n", loc)
    if nextCR >= 0:
        return strg[lastCR + 1:nextCR]
    else:
        return strg[lastCR + 1:]


def line(x1: int, y1: int, x2: int, y2: int) -> str:
    return f"dl {x1} {y1} {x2} {y2}"

