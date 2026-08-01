
def _select_with_arrows(prompt: str, choices: list[str]) -> int:
    selected = 0
    print(ANSI.bold(f"? {prompt}") + ANSI.gray("  [Use arrows, Enter to confirm]"))

    def render() -> None:
        for i, choice in enumerate(choices):
            line = ANSI.green("> ") + ANSI.bold(choice) if i == selected else "  " + choice
            sys.stdout.write(f"\r\x1b[K{line}\n")
        sys.stdout.flush()

    try:
        sys.stdout.write("\x1b[?25l")  # hide cursor
        render()
        with _raw_terminal():
            while True:
                key = _read_key()
                if key == "\x03":
                    # Ctrl+C: POSIX cbreak keeps ISIG so it never reaches here, but on Windows
                    # msvcrt.getwch() returns the raw character instead of raising.
                    raise KeyboardInterrupt
                if key == "up":
                    selected = (selected - 1) % len(choices)
                elif key == "down":
                    selected = (selected + 1) % len(choices)
                elif key.isdecimal() and 1 <= int(key) <= len(choices):
                    selected = int(key) - 1
                    break
                elif key in ("\r", "\n"):
                    break
                else:
                    continue
                sys.stdout.write(f"\x1b[{len(choices)}A")  # move back to the first option line
                render()
    finally:
        sys.stdout.write("\x1b[?25h")  # show cursor
        sys.stdout.flush()

    # Collapse the menu into a single "? prompt answer" summary line, like gh does.
    sys.stdout.write(f"\x1b[{len(choices) + 1}A\r\x1b[J")
    print(ANSI.bold(f"? {prompt} ") + ANSI.green(choices[selected]))
    return selected

