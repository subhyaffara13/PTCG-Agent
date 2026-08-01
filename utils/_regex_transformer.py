
def _regex_transformer(value: str) -> Pattern[str]:
    """Prevents 're.error' from propagating and crash pylint."""
    try:
        return re.compile(value)
    except re.error as e:
        msg = f"Error in provided regular expression: {value} beginning at index {e.pos}: {e.msg}"
        raise argparse.ArgumentTypeError(msg) from e

