import re

def _rename_without_collisions(
    name_map: dict[str, str],
    find_available: dict[str, int],
    used_names: set[str],
    orig_name: str,
    name: str,
    is_placeholder: bool = False,
):
    """
    Renames nodes to avoid name collisions, with suffixing.
    name_map: map from original name to new name
    find_available: map prefix to available suffix
    used_names: cache of used names
    orig_name: mapping key
    name: candidate name (potentially suffixed, e.g. mul_2)
    is_placeholder: if the node is a placeholder, avoid detecting suffix
    """
    match = re.match(r"(.*)_(\d+)", name)
    key = name

    if match and not is_placeholder:
        prefix, n = match.group(1), match.group(2)
        key = prefix

    new_name = name
    if new_name in used_names:
        new_name = f"{key}_{find_available[key] + 1}"

    match = re.match(r"(.*)_(\d+)", new_name)
    if match:
        prefix, n = match.group(1), match.group(2)
        if int(n) > find_available[prefix]:
            find_available[prefix] = int(n)

    name_map[orig_name] = new_name
    used_names.add(new_name)

    return name_map[orig_name]

