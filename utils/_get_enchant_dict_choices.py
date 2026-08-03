from typing import Any

def _get_enchant_dict_choices(
    inner_enchant_dicts: list[tuple[Any, enchant.ProviderDesc]],
) -> list[str]:
    return [""] + [d[0] for d in inner_enchant_dicts]

