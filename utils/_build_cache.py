
def _build_cache(name, find_available, used_names):
    used_names.add(name)
    match = re.match(r"(.*)_(\d+)", name)
    if match:
        prefix, n = match.group(1), match.group(2)
        if int(n) > find_available[prefix]:
            find_available[prefix] = int(n)

