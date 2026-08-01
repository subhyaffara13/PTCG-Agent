
def metadata_load(local_path: str | Path) -> dict | None:
    content = Path(local_path).read_text()
    match = REGEX_YAML_BLOCK.search(content)
    if match:
        yaml_block = match.group(2)
        data = yaml.safe_load(yaml_block)
        if data is None or isinstance(data, dict):
            return data
        raise ValueError("repo card metadata block should be a dict")
    else:
        return None

