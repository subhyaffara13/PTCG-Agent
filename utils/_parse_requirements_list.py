
def _parse_requirements_list(value):
    return [
        line
        for line in value.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

