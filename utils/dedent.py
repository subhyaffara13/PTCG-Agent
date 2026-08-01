
def dedent(text: str) -> str:
  r"""Wrapper around `textwrap.dedent` which also `strip()` the content.

  Before:

  ```python
  text = textwrap.dedent(
      \"\"\"\\
      A(
         x=1,
      )\"\"\"
  )
  ```

  After:

  ```python
  text = epy.dedent(
      \"\"\"
      A(
         x=1,
      )
      \"\"\"
  )
  ```

  Args:
    text: The text to dedent

  Returns:
    The dedented text
  """
  return textwrap.dedent(text).strip()

