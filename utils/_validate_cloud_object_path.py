
def _validate_cloud_object_path(object_name: str) -> None:
    if not object_name:
        raise ValueError("Cloud storage object name is required")
    if object_name.startswith("/"):
        raise ValueError("Cloud storage object name must be relative")
    if any(ord(char) < 32 or ord(char) == 127 for char in object_name):
        raise ValueError("Cloud storage object name contains control characters")
    segments = object_name.split("/")
    if any(segment in {".", ".."} for segment in segments):
        raise ValueError("Cloud storage object name contains an invalid path segment")
    if "" in segments[:-1]:
        raise ValueError("Cloud storage object name contains an invalid path segment")

