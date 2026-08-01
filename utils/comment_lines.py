
def comment_lines(lines, prefix, suffix=""):
    """Return commented lines"""
    if not prefix:
        return lines
    if not suffix:
        return [prefix + " " + line if line else prefix for line in lines]
    return [prefix + " " + line + " " + suffix if line else prefix + " " + suffix for line in lines]

