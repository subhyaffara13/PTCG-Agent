import json

def _warn_for_remote_retrieve(uri: str):
    from urllib.request import Request, urlopen
    headers = {"User-Agent": "python-jsonschema (deprecated $ref resolution)"}
    request = Request(uri, headers=headers)  # noqa: S310
    with urlopen(request) as response:  # noqa: S310
        warnings.warn(
            "Automatically retrieving remote references can be a security "
            "vulnerability and is discouraged by the JSON Schema "
            "specifications. Relying on this behavior is deprecated "
            "and will shortly become an error. If you are sure you want to "
            "remotely retrieve your reference and that it is safe to do so, "
            "you can find instructions for doing so via referencing.Registry "
            "in the referencing documentation "
            "(https://referencing.readthedocs.org).",
            DeprecationWarning,
            stacklevel=9,  # Ha ha ha ha magic numbers :/
        )
        return referencing.Resource.from_contents(
            json.load(response),
            default_specification=referencing.jsonschema.DRAFT202012,
        )

