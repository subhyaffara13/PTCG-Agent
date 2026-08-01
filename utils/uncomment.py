
def uncomment(lines, prefix="#", suffix=""):
    """Remove prefix and space, or only prefix, when possible"""
    if prefix:
        prefix_and_space = prefix + " "
        length_prefix = len(prefix)
        length_prefix_and_space = len(prefix_and_space)
        lines = [
            (
                line[length_prefix_and_space:]
                if line.startswith(prefix_and_space)
                else (line[length_prefix:] if line.startswith(prefix) else line)
            )
            for line in lines
        ]

    if suffix:
        space_and_suffix = " " + suffix
        length_suffix = len(suffix)
        length_space_and_suffix = len(space_and_suffix)
        lines = [
            (
                line[:-length_space_and_suffix]
                if line.endswith(space_and_suffix)
                else (line[:-length_suffix] if line.endswith(suffix) else line)
            )
            for line in lines
        ]

    return lines

