
def is_unexpected(name):
    """Check if this needs to be considered."""
    if '._' in name or '.tests' in name or '.setup' in name:
        return False

    if name in PUBLIC_MODULES:
        return False

    if name in PRIVATE_BUT_PRESENT_MODULES:
        return False

    return True


def is_unexpected(name):
    """Check if this needs to be considered."""
    return (
        '._' not in name and '.tests' not in name and '.setup' not in name
        and name not in PUBLIC_MODULES
        and name not in PUBLIC_ALIASED_MODULES
        and name not in PRIVATE_BUT_PRESENT_MODULES
    )

