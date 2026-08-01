
def heuristic_strip_javascript_comments(js_source: str) -> str:
  """Heuristically removes javascript comments.

  Transforms a string by removing anything between "/*" and "*/", and anything
  between "//" and the next newline. This will remove JavaScript comments. Note
  that this operates directly on the unparsed string and is not guaranteed to
  preserve the semantics of the original program (for instance, it will still
  replace "comments" that appear inside string literals). However, it works
  well enough for simple JavaScript logic.

  Args:
    js_source: String to strip comments from.

  Returns:
    Version of the input string with things that look like JavaScript comments
    removed.
  """
  no_block_comments = re.sub(
      r"/\*((?!\*/).)*\*/", "", js_source, flags=re.MULTILINE | re.DOTALL
  )
  no_line_comments = re.sub(r"//[^\n]*\n", "\n", no_block_comments)
  return no_line_comments

