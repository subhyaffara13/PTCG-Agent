
def pytest_assertrepr_compare(op, left, right):  # noqa: ARG001
    """Hook to insert custom failure explanation"""
    if hasattr(left, "explanation"):
        return left.explanation
    return None


def pytest_assertrepr_compare(
    config: Config, op: str, left: object, right: object
) -> list[str] | None:
    """Return explanation for comparisons in failing assert expressions.

    Return None for no custom explanation, otherwise return a list
    of strings. The strings will be joined by newlines but any newlines
    *in* a string will be escaped. Note that all but the first line will
    be indented slightly, the intention is for the first line to be a summary.

    :param config: The pytest config object.
    :param op: The operator, e.g. `"=="`, `"!="`, `"not in"`.
    :param left: The left operand.
    :param right: The right operand.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item's directory and its parent directories are consulted.
    """


def pytest_assertrepr_compare(
    config: Config, op: str, left: Any, right: Any
) -> list[str] | None:
    if config.pluginmanager.has_plugin("terminalreporter"):
        highlighter = config.get_terminal_writer()._highlight
    else:
        # Keep it plaintext when not using terminalrepoterer (#14377).
        highlighter = util.dummy_highlighter
    explanation = list(
        util.assertrepr_compare(
            op=op,
            left=left,
            right=right,
            verbose=config.get_verbosity(Config.VERBOSITY_ASSERTIONS),
            highlighter=highlighter,
            assertion_text_diff_style=util.get_assertion_text_diff_style(config),
        )
    )
    return explanation or None

