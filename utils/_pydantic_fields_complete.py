
def _pydantic_fields_complete(cls: type[PydanticDataclass]) -> bool:
    """Return whether the fields were successfully collected (i.e. type hints were successfully resolved).

    This is a private helper, not meant to be used outside Pydantic.
    """
    return all(field_info._complete for field_info in cls.__pydantic_fields__.values())

