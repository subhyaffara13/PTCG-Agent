
def generate_epilog(examples: list[str], docs_anchor: str | None = None) -> str:
    """Generate an epilog with examples and a Learn More section.

    Args:
        examples: List of example commands (without the `$ ` prefix).
        docs_anchor: Optional anchor for the docs URL (e.g., "#hf-download").

    Returns:
        Formatted epilog string.
    """
    docs_url = f"{CLI_REFERENCE_URL}{docs_anchor}" if docs_anchor else CLI_REFERENCE_URL
    examples_str = "\n".join(f"  $ {ex}" for ex in examples)
    return f"""\
Examples
{examples_str}

Learn more
  Use `hf <command> --help` for more information about a command.
  Read the documentation at {docs_url}
"""

