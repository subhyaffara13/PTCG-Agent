
def strip_msg(msg: str, terminal_str: str = '') -> str:
  return text.strip_msg(msg, BLOCK_MSG, BLOCK_OPT, terminal_str)


def strip_msg(msg: str, terminal_str: str = '') -> str:
  return text.strip_msg(msg, BLOCK_MSG, BLOCK_OPT, terminal_str)


def strip_msg(msg: str, terminal_str: str = '') -> str:
  return text.strip_msg(msg, BLOCK_MSG, BLOCK_OPT, terminal_str)


def strip_msg(msg: str, terminal_str: str = '') -> str:
  return text.strip_msg(msg, BLOCK_MSG, BLOCK_OPT, terminal_str)


def strip_msg(text: str,
              block_msg: str,
              block_opt: str,
              terminal_str: str = '') -> str:
  """Strip email message (with header) from text block, i.e., [ (A) - (B) ).

  Assumes messages adhere to the following format:
  BLOCK_OPT
  <-- action & info -->
  BLOCK_MSG (A)
  <-- e.g., sender/receiver -->
  BLOCK_MSG
  <-- e.g., message -->
  BLOCK_OPT (B)

  Args:
    text: str
    block_msg: str, string of characters delineating the message
    block_opt: str, string of characters demarking the start of
      the options (actions and info)
    terminal_str: str (optional), indicates the end of a message if block_opt
      is not found. this will be included in the stripped output.
  Returns:
    stripped_text: str
  """
  ctr = 0
  right_ptr = 0
  left_ptr = text.find(block_msg)
  if left_ptr == -1:
    return ''
  while ctr < 2:
    block_idx = text[right_ptr:].find(block_msg)
    if block_idx == -1:
      return ''
    right_ptr += block_idx + len(block_msg)
    ctr += 1
  block_idx = text[right_ptr:].find(block_opt)
  if block_idx != -1:  # if find block_opt return message ending at (B)
    right_ptr += block_idx
  else:
    if terminal_str:  # if no block_opt, return message ending at terminal_str
      block_idx = text[right_ptr:].find(terminal_str)
      if block_idx != -1:
        right_ptr += block_idx + len(terminal_str)
      else:  # if no terminal_str, return message to end of text string
        right_ptr = len(text)
  return text[left_ptr:right_ptr]

