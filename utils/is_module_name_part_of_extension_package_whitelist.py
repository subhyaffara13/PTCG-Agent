
def is_module_name_part_of_extension_package_whitelist(
    module_name: str, package_whitelist: set[str]
) -> bool:
    """
    Returns True if one part of the module name is in the package whitelist.

    >>> is_module_name_part_of_extension_package_whitelist('numpy.core.umath', {'numpy'})
    True
    """
    parts = module_name.split(".")
    return any(
        ".".join(parts[:x]) in package_whitelist for x in range(1, len(parts) + 1)
    )

