
def check_junit_format(choice: str) -> str:
    choices = ["global", "per_file"]
    if choice not in choices:
        raise argparse.ArgumentTypeError(
            "invalid choice '{}' (choose from {})".format(
                choice, ", ".join(f"'{x}'" for x in choices)
            )
        )
    return choice

