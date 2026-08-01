
def merge_params(original_params: list[str], new_params: list[str]) -> list[str]:
    for idx in range(len(new_params)):
        if new_params[idx] == "T":
            new_params[idx] = original_params[idx]
    return new_params

