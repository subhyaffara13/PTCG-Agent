
def _bytes_to_dataclass(cls: Any, artifact_bytes: bytes) -> Any:
    artifact_str = artifact_bytes.decode("utf-8")
    artifact_dict = json.loads(artifact_str)
    artifact_dataclass = _dict_to_dataclass(cls, artifact_dict)
    return artifact_dataclass

