
def get_overload_name_mapping(overload_info):
    # Same format as __overloads__
    # original function => [overload names]
    overload_name_mappings: dict[str, list[str]] = {}
    for orig_fn, overloads in overload_info.items():
        original_name = orig_fn.__name__
        if original_name not in overload_name_mappings:
            overload_name_mappings[original_name] = []

        for overload_name, _ in overloads:
            overload_name_mappings[original_name].append(overload_name)
    return overload_name_mappings

