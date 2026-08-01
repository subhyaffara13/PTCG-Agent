
def _create_naming_options() -> Options:
    name_options: list[tuple[str, OptionDict]] = []
    for name_type in sorted(KNOWN_NAME_TYPES):
        human_readable_name = constants.HUMAN_READABLE_TYPES[name_type]
        name_type_hyphened = name_type.replace("_", "-")

        help_msg = f"Regular expression matching correct {human_readable_name} names. "
        if name_type in KNOWN_NAME_TYPES_WITH_STYLE:
            help_msg += f"Overrides {name_type_hyphened}-naming-style. "
        help_msg += (
            f"If left empty, {human_readable_name} names will be checked "
            "with the set naming style."
        )

        # Add style option for names that support it
        if name_type in KNOWN_NAME_TYPES_WITH_STYLE:
            default_style = DEFAULT_NAMING_STYLES[name_type]
            name_options.append(
                (
                    f"{name_type_hyphened}-naming-style",
                    {
                        "default": default_style,
                        "type": "choice",
                        "choices": list(NAMING_STYLES.keys()),
                        "metavar": "<style>",
                        "help": f"Naming style matching correct {human_readable_name} names.",
                    },
                )
            )

        name_options.append(
            (
                f"{name_type_hyphened}-rgx",
                {
                    "default": None,
                    "type": "regexp",
                    "metavar": "<regexp>",
                    "help": help_msg,
                },
            )
        )
    return tuple(name_options)

