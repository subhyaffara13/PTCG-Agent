import re

def purl_from_pattern(type_, pattern, url, qualifiers=None):
    url = unquote_plus(url)
    compiled_pattern = re.compile(pattern, re.VERBOSE)
    match = compiled_pattern.match(url)

    if not match:
        return

    purl_data = {
        field: value for field, value in match.groupdict().items() if field in PackageURL._fields
    }

    qualifiers = qualifiers or {}
    # Include the `version_prefix` as a qualifier to infer valid URLs in purl2url
    version_prefix = match.groupdict().get("version_prefix")
    if version_prefix:
        qualifiers.update({"version_prefix": version_prefix})

    if qualifiers:
        if "qualifiers" in purl_data:
            purl_data["qualifiers"].update(qualifiers)
        else:
            purl_data["qualifiers"] = qualifiers

    return PackageURL(type_, **purl_data)

