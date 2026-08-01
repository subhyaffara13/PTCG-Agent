
def _validate_driver_name(name: str) -> None:
    """Validate an upstream driver name.

    The name should look like a typical Python distribution or package name,
    following a simplified form of PEP 503 normalisation rules:

    * start with a lowercase ASCII letter
    * contain only lowercase letters, digits, hyphens and underscores

    Examples of valid names: ``"django-redis"``, ``"celery"``, ``"rq"``.
    """

    import re

    _validate_no_invalid_chars(name, "Driver name")
    if not re.match(r"^[a-z][a-z0-9_-]*$", name):
        raise ValueError(
            "Upstream driver name must use a Python package-style name: "
            "start with a lowercase letter and contain only lowercase letters, "
            "digits, hyphens, and underscores (e.g., 'django-redis')."
        )

