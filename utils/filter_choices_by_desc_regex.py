import re

def filter_choices_by_desc_regex(choices: list[ChoiceCaller]) -> list[ChoiceCaller]:
    """Filter choices based on autotune_choice_desc_regex config."""
    if config.test_configs.autotune_choice_desc_regex is not None:
        return [
            c
            for c in choices
            if re.search(
                config.test_configs.autotune_choice_desc_regex,
                c.description,
            )
        ]
    return choices

