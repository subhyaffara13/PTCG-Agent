
def _expect_regex(controller, regex):
  """Reads a line from the controller, parses it using the regular expression."""
  line = controller.read_line()
  match = re.match(regex, line)
  if not match:
    raise ValueError("Received '{}' which does not match regex '{}'".format(
        line, regex))
  return match.groupdict()


def _expect_regex(client, regex):
  """Reads a line from the client, parses it using the regular expression."""
  line = client.read_line()
  match = re.match(regex, line)
  if not match:
    raise ValueError("Received '{}' which does not match regex '{}'".format(
        line, regex))
  return match.groupdict()

