
def validate_package_allow_list(allow_list: list[str]) -> list[str]:
    for p in allow_list:
        msg = f"Invalid allow list entry: {p}"
        if "*" in p:
            raise argparse.ArgumentTypeError(
                f"{msg} (entries are already prefixes so must not contain *)"
            )
        if "\\" in p or "/" in p:
            raise argparse.ArgumentTypeError(
                f"{msg} (entries must be packages like foo.bar not directories or files)"
            )
    return allow_list

