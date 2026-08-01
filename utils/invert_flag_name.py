
def invert_flag_name(flag: str) -> str:
    split = flag[2:].split("-", 1)
    if len(split) == 2:
        prefix, rest = split
        if prefix in flag_prefix_map:
            return f"--{flag_prefix_map[prefix]}-{rest}"
        elif prefix == "no":
            return f"--{rest}"

    return f"--no-{flag[2:]}"

