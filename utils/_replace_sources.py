from typing import Any

def _replace_sources(result_str: str, flat_input_paths: list[Any]):
    """
    Given user specified input paths, maybe fix up the guard string
    to reflect user path instead of tracer path.
    """
    name_mapping = {}
    for idx, path in enumerate(flat_input_paths):
        name_mapping[f"L['flat_args'][{idx}]"] = f"L{pytree.keystr(path)}"

    replace = result_str
    for key, val in name_mapping.items():
        replace = replace.replace(key, val)
    return replace

