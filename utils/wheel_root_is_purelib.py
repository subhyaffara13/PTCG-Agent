
def wheel_root_is_purelib(metadata: Message) -> bool:
    return metadata.get("Root-Is-Purelib", "").lower() == "true"

