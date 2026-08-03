import re

def is_active(ext, metadata, default=True):
    """Is the cell active for the given file extension?"""
    if metadata.get("run_control", {}).get("frozen") is True:
        return ext == ".ipynb"
    for tag in metadata.get("tags", []):
        if tag.startswith("active-"):
            return ext.replace(".", "") in tag.split("-")
    if "active" not in metadata:
        return default
    return ext.replace(".", "") in re.split(r"\.|,", metadata["active"])

