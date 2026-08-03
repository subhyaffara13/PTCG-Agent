import re

def filter_choices_by_name_regex(choices: list[ChoiceCaller]) -> list[ChoiceCaller]:
    """Filter choices based on autotune_choice_name_regex config."""
    if config.test_configs.autotune_choice_name_regex is not None:
        return [
            c
            for c in choices
            if re.search(
                config.test_configs.autotune_choice_name_regex,
                c.name,
            )
        ]
    return choices

