
def add_test_name_suffix(name: str, suffix: str) -> str:
    # Find magic suffix of form "-foobar" (used for things like "-skip").
    m = re.search(r"-[-A-Za-z0-9]+$", name)
    if m:
        # Insert suite-specific test name suffix before the magic suffix
        # which must be the last thing in the test case name since we
        # are using endswith() checks.
        magic_suffix = m.group(0)
        return name[: -len(magic_suffix)] + suffix + magic_suffix
    else:
        return name + suffix

