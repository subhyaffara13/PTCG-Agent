
def select_choice(prompt: str, choices: list[str]) -> int:
    """Single-choice interactive prompt. Returns the index of the selected choice.

    On a TTY, renders an arrow-key menu (Up/Down to move, Enter to confirm, 1-9 to pick
    directly, Ctrl+C to abort). Falls back to a numbered `input()` prompt when raw
    keyboard input is not available. Callers are responsible for not prompting at all in
    non-interactive contexts.
    """
    if not choices:
        raise ValueError("select_choice() requires at least one choice.")
    if _supports_raw_keyboard():
        return _select_with_arrows(prompt, choices)
    return _select_with_numbers(prompt, choices)

