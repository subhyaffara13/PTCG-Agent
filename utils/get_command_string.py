import os

def get_command_string(command):
  """Returns an escaped string that can be used as a shell command.

  Args:
    command: List or string representing the command to run.
  Returns:
    A string suitable for use as a shell command.
  """
  if isinstance(command, str):
    return command
  else:
    if os.name == 'nt':
      return ' '.join(command)
    else:
      # The following is identical to Python 3's shlex.quote function.
      command_string = ''
      for word in command:
        # Single quote word, and replace each ' in word with '"'"'
        command_string += "'" + word.replace("'", "'\"'\"'") + "' "
      return command_string[:-1]

