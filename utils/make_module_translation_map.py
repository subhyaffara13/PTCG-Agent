
def make_module_translation_map(names: list[str]) -> dict[str, str]:
    num_instances: dict[str, int] = {}
    for name in names:
        for suffix in candidate_suffixes(name):
            num_instances[suffix] = num_instances.get(suffix, 0) + 1
    result = {}
    for name in names:
        for suffix in candidate_suffixes(name):
            if num_instances[suffix] == 1:
                break
        # Takes the last suffix if none are unique
        result[name] = suffix
    return result

