
def _preprocess_options(run: Run, args: Sequence[str]) -> list[str]:
    """Pre-process options before full config parsing has started."""
    processed_args: list[str] = []

    i = 0
    while i < len(args):
        argument = args[i]
        if not argument.startswith("-"):
            processed_args.append(argument)
            i += 1
            continue

        try:
            option, value = argument.split("=", 1)
        except ValueError:
            option, value = argument, None

        matched_option = None
        for option_name, data in PREPROCESSABLE_OPTIONS.items():
            to_match = data[2]
            if to_match == 0:
                if option == option_name:
                    matched_option = option_name
            elif option.startswith(option_name[:to_match]):
                matched_option = option_name

        if matched_option is None:
            processed_args.append(argument)
            i += 1
            continue

        takearg, cb, _ = PREPROCESSABLE_OPTIONS[matched_option]

        if takearg and value is None:
            i += 1
            if i >= len(args) or args[i].startswith("-"):
                raise ArgumentPreprocessingError(f"Option {option} expects a value")
            value = args[i]
        elif not takearg and value is not None:
            raise ArgumentPreprocessingError(f"Option {option} doesn't expect a value")

        cb(run, value)
        i += 1

    return processed_args

