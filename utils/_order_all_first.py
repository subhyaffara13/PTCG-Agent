
def _order_all_first(config_args: list[str], *, joined: bool) -> list[str]:
    """Reorder config_args such that --enable=all or --disable=all comes first.

    Raise if both are given.

    If joined is True, expect args in the form '--enable=all,for-any-all'.
    If joined is False, expect args in the form '--enable', 'all,for-any-all'.
    """
    indexes_to_prepend = []
    all_action = ""

    for i, arg in enumerate(config_args):
        if joined and arg.startswith(("--enable=", "--disable=")):
            value = arg.split("=")[1]
        elif arg in {"--enable", "--disable"}:
            value = config_args[i + 1]
        else:
            continue

        if "all" not in (msg.strip() for msg in value.split(",")):
            continue

        arg = arg.split("=")[0]
        if all_action and (arg != all_action):
            raise ArgumentPreprocessingError(
                "--enable=all and --disable=all are incompatible."
            )
        all_action = arg

        indexes_to_prepend.append(i)
        if not joined:
            indexes_to_prepend.append(i + 1)

    returned_args = []
    for i in indexes_to_prepend:
        returned_args.append(config_args[i])

    for i, arg in enumerate(config_args):
        if i in indexes_to_prepend:
            continue
        returned_args.append(arg)

    return returned_args

