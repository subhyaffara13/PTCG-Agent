
def _qualifier_map_to_string(qualifiers: dict[str, str]) -> str:
    qualifiers_list = [f"{key}={value}" for key, value in qualifiers.items()]
    return "&".join(qualifiers_list)

