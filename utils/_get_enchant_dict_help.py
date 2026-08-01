
def _get_enchant_dict_help(
    inner_enchant_dicts: list[tuple[Any, enchant.ProviderDesc]],
    pyenchant_available: bool,
) -> str:
    if inner_enchant_dicts:
        dict_as_str = [f"{d[0]} ({d[1].name})" for d in inner_enchant_dicts]
        enchant_help = f"Available dictionaries: {', '.join(dict_as_str)}"
    else:
        enchant_help = "No available dictionaries : You need to install "
        if not pyenchant_available:
            enchant_help += "both the python package and "
        enchant_help += "the system dependency for enchant to work"
    return f"Spelling dictionary name. {enchant_help}."

