
def clear_field(message: Message, field_name: Text) -> None:
  """Clears the contents of a given field.

  Inside a oneof group, clears the field set. If the name neither refers to a
  defined field or oneof group, :exc:`ValueError` is raised.

  Args:
    message: The proto message.
    field_name (str): The name of the field to be cleared.

  Raises:
    ValueError: if the `field_name` is not a member of this message.
  """
  message.ClearField(field_name)

