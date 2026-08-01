
def purl_to_lookups(purl_str, encode=True, include_empty_fields=False):
    """
    Return a lookups dictionary built from the provided `purl` (Package URL) string.
    These lookups can be used as QuerySet filters.
    If include_empty_fields is provided, the resulting dictionary will include fields
    with empty values. This is useful to get exact match.
    Note that empty values are always returned as empty strings as the model fields
    are defined with `blank=True` and `null=False`.
    """
    if not purl_str.startswith("pkg:"):
        purl_str = "pkg:" + purl_str

    try:
        package_url = PackageURL.from_string(purl_str)
    except ValueError:
        return  # Not a valid PackageURL

    package_url_dict = package_url.to_dict(encode=encode, empty="")
    if include_empty_fields:
        return package_url_dict
    else:
        return without_empty_values(package_url_dict)

