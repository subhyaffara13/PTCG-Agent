import re

def get_chexify_err_regex(name, msg):
  return re.escape(_ai.get_chexify_err_message(name, 'ANY')).replace(
      'ANY', f'.*{msg}.*'
  )

