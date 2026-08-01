
def _get_mem_divisor(units: str) -> int:
    unit_dict = {"B": 1, "KiB": 2**10, "MiB": 2**20, "GiB": 2**30}
    if units in unit_dict:
        return unit_dict[units]
    else:
        raise ValueError(
            f"Unsupported unit: {units}. Supported units are: {', '.join(unit_dict.keys())}"
        )

