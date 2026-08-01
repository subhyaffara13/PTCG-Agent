
def check_follow_imports(choice: str) -> str:
    choices = ["normal", "silent", "skip", "error"]
    if choice not in choices:
        raise argparse.ArgumentTypeError(
            "invalid choice '{}' (choose from {})".format(
                choice, ", ".join(f"'{x}'" for x in choices)
            )
        )
    return choice

