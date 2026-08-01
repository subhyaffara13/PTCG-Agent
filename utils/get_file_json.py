
def get_file_json(path: str | Path, fallback: Any | None = None) -> Any:
    try:
        with open(path, "r") as json_file:
            return json.load(json_file)
    except Exception:
        if fallback is not None:
            return fallback
        raise InvalidArgument(f"{path} does not contain valid JSON")

