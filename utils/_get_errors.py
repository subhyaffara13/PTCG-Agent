from typing import Any

def _get_errors(
    nbdict: Any, version: int, version_minor: int, relax_add_props: bool, *args: Any
) -> Any:
    validator = get_validator(version, version_minor, relax_add_props=relax_add_props)
    if not validator:
        msg = f"No schema for validating v{version}.{version_minor} notebooks"
        raise ValidationError(msg)
    iter_errors = validator.iter_errors(nbdict, *args)
    errors = list(iter_errors)
    # jsonschema gives the best error messages.
    if len(errors) and validator.name != "jsonschema":
        validator = get_validator(
            version=version,
            version_minor=version_minor,
            relax_add_props=relax_add_props,
            name="jsonschema",
        )
        return validator.iter_errors(nbdict, *args)
    return iter(errors)

