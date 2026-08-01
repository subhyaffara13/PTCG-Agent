
def _reverse_map(d: dict[Any, Enum]):
    return {v.value: k for k, v in d.items()}

