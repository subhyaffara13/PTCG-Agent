
def _is_bogus_const_name(name: str):
    splitted_names = name.split(".")
    if len(splitted_names) < 1:
        return True

    return splitted_names[-1].startswith("lifted_tensor")

