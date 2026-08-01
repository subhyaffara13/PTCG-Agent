
def convert_to_dict(message: Union[BaseModel, dict]) -> dict:
    """
    Converts a message to a dictionary if it's a Pydantic model.

    Args:
        message: The message, which may be a Pydantic model or a dictionary.

    Returns:
        dict: The converted message.
    """
    if isinstance(message, BaseModel):
        return message.model_dump(exclude_none=True)  # type: ignore
    elif isinstance(message, dict):
        return message
    else:
        raise TypeError(
            f"Invalid message type: {type(message)}. Expected dict or Pydantic model."
        )

