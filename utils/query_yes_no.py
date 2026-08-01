
def query_yes_no(question: str, default: str = "yes") -> bool:  # Defensive:
    """Ask a yes/no question via input() and return the answer as a bool."""
    prompt = " [Y/n] " if default == "yes" else " [y/N] "

    while True:
        choice = input(question + prompt).strip().lower()
        if not choice:
            return default == "yes"
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Please respond with 'y' or 'n'.")

