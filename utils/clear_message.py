
def clear_message(message: Message) -> None:
  """Clears all data that was set in the message.

  Args:
    message: The proto message to be cleared.
  """
  message.Clear()

