import sys

def _prompt_login_method() -> str:
    """Ask the user how to log in: "browser" (default) or "token". Never prompts without a TTY."""
    if sys.stdin is None or not sys.stdin.isatty():
        return "browser"
    choice = select_choice("How would you like to log in?", ["Log in with your browser", "Paste an access token"])
    return "browser" if choice == 0 else "token"

