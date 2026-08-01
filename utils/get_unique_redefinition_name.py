
def get_unique_redefinition_name(name: str, existing: Container[str]) -> str:
    """Get a simple redefinition name not present among existing.

    For example, for name 'foo' we try 'foo-redefinition', 'foo-redefinition2',
    'foo-redefinition3', etc. until we find one that is not in existing.
    """
    r_name = name + "-redefinition"
    if r_name not in existing:
        return r_name

    i = 2
    while r_name + str(i) in existing:
        i += 1
    return r_name + str(i)

