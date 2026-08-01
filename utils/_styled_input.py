
def _styled_input(prompt: str) -> str:
    """
    Like input() but wraps ANSI sequences in readline ignore markers
    (\\001...\\002) so readline correctly tracks the cursor column.
    In non-TTY contexts, strips ANSI entirely so no escape codes appear.
    """
    if sys.stdout.isatty():
        rl_prompt = _ANSI_RE.sub(lambda m: f"\001{m.group()}\002", prompt)
    else:
        rl_prompt = _ANSI_RE.sub("", prompt)
    return input(rl_prompt).strip()

