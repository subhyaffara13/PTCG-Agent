
def _detect_trailing_regex() -> re.Pattern[str]:
  """Check if the last character is a `;` token."""
  # Match:
  # * `; a`
  # * `; a # Some comment`
  # * `; # Some comment`
  # Do not match:
  # * `; a; b`
  # * `; a=1`

  available_letters = ''.join(sorted(_Options.all_letters))  # pytype: disable=wrong-arg-types
  return re.compile(
      ' *; *'  # Trailing `;` (surrounded by spaces)
      f'(?P<options>[{available_letters}]*)?'  # Optionally a `option` letter
      ' *(?:#.*)?$'  # Line can end by a `# comment`
  )

