
def result_exists(set_key, case):
    """Searches the results dict for a result in the set that matches a case.
    Returns True if such a case exists."""
    if set_key not in res_dict:
        raise ValueError(f"{set_key} not present in data structure!")

    case_dict = to_dict(case)
    existing_res = list(filter(
        lambda res: res["src_case"] == case_dict,  # dict comparison
        res_dict[set_key]))

    return len(existing_res) > 0

