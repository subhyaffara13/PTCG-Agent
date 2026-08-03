import re

def normalize_file_output(content: list[str], current_abs_path: str) -> list[str]:
    """Normalize file output for comparison."""
    timestamp_regex = re.compile(r"\d{10}")
    result = [x.replace(current_abs_path, "$PWD") for x in content]
    version = mypy.version.__version__
    result = [re.sub(r"\b" + re.escape(version) + r"\b", "$VERSION", x) for x in result]
    # We generate a new mypy.version when building mypy wheels that
    # lacks base_version, so handle that case.
    base_version = getattr(mypy.version, "base_version", version)
    result = [re.sub(r"\b" + re.escape(base_version) + r"\b", "$VERSION", x) for x in result]
    result = [timestamp_regex.sub("$TIMESTAMP", x) for x in result]
    return result

