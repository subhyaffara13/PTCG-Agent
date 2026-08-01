
def _normalise_cmd_options(desc: _OptionsList) -> set[str]:
    return {_normalise_cmd_option_key(fancy_option[0]) for fancy_option in desc}

